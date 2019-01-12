@echo off
set setting_file = "%cd%/.vscode/settings.json"
FOR /F "tokens=* USEBACKQ" %%F IN (`python "U:\tools\internal\workflowtools\read_settings.py" "%cd%"`) DO (
SET var=%%F
)
echo %var%