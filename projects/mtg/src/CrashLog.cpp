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
static LONG WINAPI wagicCrashFilter(EXCEPTION_POINTERS* info)
{
    unsigned long code = (info && info->ExceptionRecord) ? info->ExceptionRecord->ExceptionCode : 0;
    char reason[80];
    _snprintf(reason, sizeof(reason), "Unhandled exception 0x%08lx", code);
    reason[sizeof(reason) - 1] = '\0';
    CrashLog::logCrash(reason);
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
