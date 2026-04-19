@echo off
echo Signing APK with debug keystore...
C:\Android-SDK\build-tools\26.0.3\apksigner.bat sign ^
  --ks "%USERPROFILE%\.android\debug.keystore" ^
  --ks-pass pass:android ^
  --key-pass pass:android ^
  --ks-key-alias androiddebugkey ^
  --out "M:\Claude_projects\wagic\projects\mtg\Android\bin\Wagic-debug.apk" ^
  "M:\Claude_projects\wagic\projects\mtg\Android\bin\apk_work\Wagic-unsigned.apk"
echo Done. Exit code: %ERRORLEVEL%
pause
