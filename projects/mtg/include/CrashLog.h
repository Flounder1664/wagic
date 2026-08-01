#ifndef _CRASHLOG_H_
#define _CRASHLOG_H_

#include <string>

// Lightweight breadcrumb + crash logger.
//
// The Release Windows build compiles DebugTrace to nothing and has no crash
// handler, so a card-ability crash just closes the game with no trace and no
// way to tell which card was at fault. This keeps a small ring buffer of the
// most recent in-game actions (set from ActionStack::resolve, the central
// resolution chokepoint) and, on an unhandled exception, appends them to
// crash_log.txt next to the executable -- so the offending card can be
// identified and its primitive fixed.
//
// The log is append-only across runs (each crash adds a block); clear the file
// by hand once a card is fixed. No-op on platforms without the handler.
namespace CrashLog
{
    void setBreadcrumb(const std::string& crumb);
    void logCrash(const std::string& reason);
    void install(); // install the platform crash handler; call once at startup
}

#endif
