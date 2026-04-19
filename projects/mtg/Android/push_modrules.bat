@echo off
setlocal

set ADB=C:\Android-SDK\platform-tools\adb.exe
set SRC=M:\Claude_projects\wagic\projects\mtg\bin\Res\rules\modrules.xml

echo Checking device connection...
%ADB% devices

echo.
echo Trying /sdcard/Wagic/Res/rules/
%ADB% shell "ls /sdcard/Wagic/Res/rules/" 2>nul
if %ERRORLEVEL% == 0 (
    echo Found! Pushing to /sdcard/Wagic/Res/rules/modrules.xml
    %ADB% push "%SRC%" /sdcard/Wagic/Res/rules/modrules.xml
    goto done
)

echo Trying /sdcard/Android/data/net.wagic.app/files/Wagic/Res/rules/
%ADB% shell "ls /sdcard/Android/data/net.wagic.app/files/Wagic/Res/rules/" 2>nul
if %ERRORLEVEL% == 0 (
    echo Found! Pushing to /sdcard/Android/data/net.wagic.app/files/Wagic/Res/rules/modrules.xml
    %ADB% push "%SRC%" /sdcard/Android/data/net.wagic.app/files/Wagic/Res/rules/modrules.xml
    goto done
)

echo.
echo Could not find Wagic rules folder automatically.
echo Please check adb shell ls /sdcard/ for the correct path,
echo or manually copy modrules.xml using Windows Explorer.
echo Source file: %SRC%
goto end

:done
echo.
echo Done. Restart Wagic on the device to pick up the change.

:end
pause
