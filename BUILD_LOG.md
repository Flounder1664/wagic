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
```
