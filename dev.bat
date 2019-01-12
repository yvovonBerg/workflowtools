@echo off

:: read vs code settings file
set setting_file = "%cd%/.vscode/settings.json"
FOR /F "tokens=* USEBACKQ" %%F IN (`python "U:\tools\internal\workflowtools\read_settings.py" "%cd%"`) DO (
    SET var=%%F
)
"%var%/activate" >nul 2>&1

:: use current directory as fallback
for %%I in (.) do set folder=%%~nxI
"U:\virtual_envs\%folder%\Scripts\activate" >nul 2>&1
