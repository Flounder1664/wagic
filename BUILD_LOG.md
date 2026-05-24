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
2026-05-07 6a26c874d                device=Windows result=pass — Quick Game now shows land icon (mIcons[12] + i<6 + modrules.xml iconId=6)
2026-05-07 6a26c874d                device=S9      result=pass — same after pushing modrules.xml to /storage/0449-B4A1/.../Wagic/Res/rules/
2026-05-07 6a26c874d                device=RP5     result=pass — same after pushing modrules.xml to /storage/3963-3235/.../Wagic/Res/rules/
2026-05-07 f65a30263                device=Windows result=pass — delete-deck + version-display 0.25.7 (resource 0.25.6) verified
2026-05-07 f65a30263                device=S9      result=pass — same; pushed Wagic-core-0256.zip to SD UUID 0449-B4A1
2026-05-07 f65a30263                device=RP5     result=pass — same; refreshed Wagic-core-0256.zip (May-4 58 MB build)
2026-05-10 feature/duskmourn-rooms  device=Windows result=build-pass — VS2022 v145 Release/Win32 builds clean (7 warnings, 0 errors); Wagic.exe + Wagic-core-0256.zip + DSK 673448 image deployed to G:\Wagic-windows\; gameplay verification pending
2026-05-25 34b8ade5b (wagic-v146-windows)  device=Windows result=build-pass — VS2022 v145 Release/Win32 builds clean (0 warnings, 0 errors); baseline merges feature/duskmourn-rooms + wip/card-data-may; Wagic.exe + Wagic-core-0257.zip deployed to G:\Wagic-windows\; collection rebuilt (41,701 unique-art IDs × 4 = 166,804 entries); Wagic-core-0256.zip retired to .old
```
