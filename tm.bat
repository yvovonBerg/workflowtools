@echo off
PUSHD %CD%
cd /D "U:\tools\internal\workflowtools"
dev.bat && python "U:\tools\internal\workflowtools\time_manager\time_manager\time_manager.py" %* && q && POPD

