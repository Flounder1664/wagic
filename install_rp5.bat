@echo off
echo Uninstalling existing Wagic...
C:\Android-SDK\platform-tools\adb.exe -s d15e0854 uninstall net.wagic.app
echo Uninstall result: %ERRORLEVEL%

echo.
echo Installing new APK...
C:\Android-SDK\platform-tools\adb.exe -s d15e0854 install "M:\Claude_projects\wagic\projects\mtg\Android\bin\Wagic-debug.apk"
echo Install result: %ERRORLEVEL%
pause
