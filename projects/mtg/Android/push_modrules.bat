@echo off
setlocal

set ADB=C:\Android-SDK\platform-tools\adb.exe
set SRC=M:\Claude_projects\wagic\projects\mtg\bin\Res\rules\modrules.xml

echo Checking device connection...
%ADB% devices

echo.
echo Searching for Wagic rules folder on device...

for /f "delims=" %%P in ('%ADB% shell "find /storage -name modrules.xml 2>/dev/null | head -1"') do set FOUND=%%P

if not defined FOUND (
    echo Not found via find, trying known paths...
    for /f "delims=" %%P in ('%ADB% shell "find /sdcard /storage/emulated/0 -maxdepth 5 -name modrules.xml 2>/dev/null | head -1"') do set FOUND=%%P
)

if not defined FOUND (
    echo ERROR: Could not find modrules.xml on device.
    echo Make sure Wagic has been launched at least once to create its data folders.
    goto end
)

echo Found at: %FOUND%
%ADB% push "%SRC%" "%FOUND%"
if %ERRORLEVEL% == 0 (
    echo Done. Restart Wagic on the device to pick up the change.
) else (
    echo Push failed.
)

:end
pause
