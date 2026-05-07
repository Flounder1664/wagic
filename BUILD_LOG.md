# Build / install log

Append-only. One line per device install or notable build.

Format: `YYYY-MM-DD <commit-or-tag>  device=<RP5|S9|Windows>  result=<pass|fail-detail>`

Device serials:
- RP5 = `d15e0854`
- S9 Tablet = `R52X10ACZCW`

```
2026-04-19 64833c619               device=RP5     result=pass — swipe fix verified
2026-04-19 64833c619               device=S9      result=pass — swipe fix verified (tag verified-android-2026-04-19)
2026-04-24 wagic-v145-windows-tip  device=Windows result=pass — VS2022 v145 build clean
2026-05-XX wagic-v145-windows-tip  device=S9      result=fail — taps not registering, sluggish (regression)
2026-05-07 41c82285c               device=S9      result=fail — SIGSEGV in libgui BufferQueue ~14s into launch (pre-Phase-1 baseline)
2026-05-07 wagic-v145-windows-tip  device=S9      result=fail — same SIGSEGV (rules out Phase 1 cherry-pick as cause)
2026-05-07 verified-android-2026-04-19  device=S9 result=fail — same SIGSEGV (rules out post-Apr-24 commits as crash cause)
2026-05-07 verified-android-2026-04-19  device=S9 result=pass — after `pm clear net.wagic.app`; root cause was internal app data corruption
2026-05-07 41c82285c               device=S9      result=partial — boots cleanly after data clear, but taps problematic (separate code regression, no quickplay due to outdated core.zip)
2026-05-07 41c82285c               device=S9      result=partial — quickplay restored after pushing PC core.zip; taps still problematic (real code regression in 7a32a6f30 confirmed)
2026-05-07 41c82285c               device=RP5     result=pass — process alive, gamepad + features all good
2026-05-07 e1db9f205             device=S9      result=pass — taps work after scoping joystick init `#ifndef ANDROID`
2026-05-07 e1db9f205             device=RP5     result=pass — gamepad still works (SDL joystick path was unused on RP5; gamepad goes via Java keysyms)
2026-05-07 e1db9f205             device=Windows result=pass — VS2022 v145 Release/Win32 builds Wagic.exe; #ifndef ANDROID is no-op on Windows
```
