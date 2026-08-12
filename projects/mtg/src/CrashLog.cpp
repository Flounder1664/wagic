#include "PrecompiledHeader.h"

#include "CrashLog.h"

#include <cstdio>
#include <ctime>

#if defined(WIN32)
#include <windows.h>
#endif

namespace
{
// Small ring buffer of the most recent breadcrumbs. Fixed-size and static so
// it needs no allocation at crash time (the heap may be in a fragile state).
const int kMaxCrumbs = 12;
std::string gCrumbs[kMaxCrumbs];
int gCrumbHead = 0; // index of the next write
int gCrumbCount = 0;

// Relative to the working directory -- for the Windows build that's the
// install root (next to Wagic.exe), where the player can easily find it.
const char* kLogPath = "crash_log.txt";
}

void CrashLog::setBreadcrumb(const std::string& crumb)
{
    gCrumbs[gCrumbHead] = crumb;
    gCrumbHead = (gCrumbHead + 1) % kMaxCrumbs;
    if (gCrumbCount < kMaxCrumbs)
        gCrumbCount++;
}

void CrashLog::logCrash(const std::string& reason)
{
    FILE* f = fopen(kLogPath, "a");
    if (!f)
        return;

    time_t now = time(NULL);
    struct tm* lt = localtime(&now);
    char ts[64] = "unknown time";
    if (lt)
        strftime(ts, sizeof(ts), "%Y-%m-%d %H:%M:%S", lt);

    fprintf(f, "\n=== CRASH %s ===\n", ts);
    fprintf(f, "Reason: %s\n", reason.c_str());
    fprintf(f, "Recent actions (oldest first, newest is likely the culprit):\n");

    int start = (gCrumbCount < kMaxCrumbs) ? 0 : gCrumbHead;
    for (int i = 0; i < gCrumbCount; i++)
    {
        int idx = (start + i) % kMaxCrumbs;
        fprintf(f, "  %s\n", gCrumbs[idx].c_str());
    }
    if (gCrumbCount == 0)
        fprintf(f, "  (no in-game actions recorded)\n");

    fclose(f);
}

#if defined(WIN32)
// Append the faulting address and a stack walk, as module+offset lines.
// The breadcrumbs say WHEN a crash happened (which game action) but never
// WHERE. That left GUI-only crashes undiagnosable, because the console
// TestSuite build does no rendering and so cannot reach them at all -- a green
// harness run is not evidence about the GUI path.
// CaptureStackBackTrace is kernel32-only: no dbghelp, no Debugging Tools
// install, nothing to configure. Map a line like "Wagic.exe+0x1a2b3c" back to
// source using the build's .map/.pdb.
static void appendCrashStack(EXCEPTION_POINTERS* info)
{
    FILE* f = fopen("crash_log.txt", "a");
    if (!f)
        return;

    if (info && info->ExceptionRecord)
    {
        fprintf(f, "Faulting address: 0x%p\n", info->ExceptionRecord->ExceptionAddress);
        // For an access violation the first two parameters say read vs write, and the target.
        if (info->ExceptionRecord->ExceptionCode == EXCEPTION_ACCESS_VIOLATION &&
            info->ExceptionRecord->NumberParameters >= 2)
        {
            fprintf(f, "Access violation: %s address 0x%p\n",
                    info->ExceptionRecord->ExceptionInformation[0] ? "write to" : "read from",
                    (void*)info->ExceptionRecord->ExceptionInformation[1]);
        }
    }

    void* frames[48];
    USHORT n = CaptureStackBackTrace(0, 48, frames, NULL);
    fprintf(f, "Stack (%u frames, innermost first):\n", (unsigned)n);
    for (USHORT i = 0; i < n; i++)
    {
        HMODULE mod = NULL;
        if (GetModuleHandleExA(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS | GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
                               (LPCSTR)frames[i], &mod) && mod)
        {
            char full[MAX_PATH];
            const char* shortName = "?";
            if (GetModuleFileNameA(mod, full, MAX_PATH))
            {
                const char* slash = strrchr(full, '\\');
                shortName = slash ? slash + 1 : full;
            }
            fprintf(f, "  %-20s +0x%lx\n", shortName,
                    (unsigned long)((char*)frames[i] - (char*)mod));
        }
        else
        {
            fprintf(f, "  %-20s 0x%p\n", "(unknown module)", frames[i]);
        }
    }
    fclose(f);
}

static LONG WINAPI wagicCrashFilter(EXCEPTION_POINTERS* info)
{
    unsigned long code = (info && info->ExceptionRecord) ? info->ExceptionRecord->ExceptionCode : 0;
    char reason[80];
    _snprintf(reason, sizeof(reason), "Unhandled exception 0x%08lx", code);
    reason[sizeof(reason) - 1] = '\0';
    CrashLog::logCrash(reason);
    appendCrashStack(info);
    return EXCEPTION_EXECUTE_HANDLER; // log written; let the process terminate
}

void CrashLog::install()
{
    SetUnhandledExceptionFilter(wagicCrashFilter);
}
#else
void CrashLog::install()
{
}
#endif
