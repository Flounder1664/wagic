@echo off
C:\android-ndk-r22\ndk-build.cmd NDK_PROJECT_PATH=M:\Claude_projects\wagic\projects\mtg\Android NDK_APPLICATION_MK=M:\Claude_projects\wagic\projects\mtg\Android\jni\Application.mk %* > M:\ndk_build_log.txt 2>&1
echo Exit code: %ERRORLEVEL% >> M:\ndk_build_log.txt
