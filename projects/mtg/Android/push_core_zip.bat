@echo off
setlocal

set ADB=C:\Android-SDK\platform-tools\adb.exe
set SRC=M:\Claude_projects\wagic\projects\mtg\bin\Res\Wagic-core-0256.zip
set ZIPNAME=Wagic-core-0256.zip

echo Checking device connection...
%ADB% devices

echo.
echo Searching for Wagic Res folder on device...

for /f "delims=" %%P in ('%ADB% shell "find /storage -name "Wagic-core*.zip" 2>/dev/null | head -1"') do set FOUND=%%P

if not defined FOUND (
    echo No existing zip found - searching for Wagic/Res directory...
    for /f "delims=" %%P in ('%ADB% shell "find /storage -type d -name Res -path "*/Wagic/Res*" 2>/dev/null | head -1"') do set RESDIR=%%P
) else (
    for /f "delims=" %%P in ('%ADB% shell "dirname \"%FOUND%\""') do set RESDIR=%%P
)

if not defined RESDIR (
    echo ERROR: Could not find Wagic/Res folder on device.
    echo Make sure Wagic has been launched at least once to create its data folders.
    goto end
)

echo Pushing %ZIPNAME% to %RESDIR%...
%ADB% push "%SRC%" "%RESDIR%/%ZIPNAME%"
if %ERRORLEVEL% == 0 (
    echo Done.
    %ADB% shell "ls -la \"%RESDIR%\""
) else (
    echo Push failed.
)

:end
pause
