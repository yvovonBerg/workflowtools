@echo off
setlocal EnableDelayedExpansion
if not "%~1"=="" (
    ffmpeg -ss "%~2" -i "%~1" -t 500 -c copy "out.mp4" -y >nul 2>&1
    "out.mp4"
    goto endoffile
) 
set /p inputcfile="Enter filepath: " || set "inputcfile="
set /p outputcfile="Enter outputfile(outfile.mp4): " || set "outputcfile=outfile.mp4"
set /p cutdurationc="Enter duration (ms): " || set "cutdurationc="
set /p fullduration="Enter clip duration (ms, 100): " || set "fullduration=100"

ffmpeg -ss %cutdurationc% -i "%inputcfile%" -t %fullduration% -c copy %outputcfile% -y 
%outputcfile%

:endoffile