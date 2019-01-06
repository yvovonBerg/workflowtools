@echo off
set /p root="Enter root path: "
set /p new_git_repo="Make new git repo [y/n]: "
set /p name="Enter project name: "
set /p is_python="Python project: [y/n]: "
set /p new_venv="Make new virtual env: [y/n]: "

IF NOT EXIST %root% ( mkdir %root% )
cd /D "%root%"
:: python stuff
IF "%is_python%" == "y" (
        IF "%new_venv%" == "y" ( 
			virtualenv U:\virtual_envs\%name%
		)
	mkdir .vscode
	cd .vscode
	echo.> settings.json
	echo { > settings.json
	echo     "python.linting.enabled": true, >> settings.json
	echo     "python.pythonPath": "U:\\virtual_envs\\%name%\\Scripts\\python.exe", >> settings.json
	echo     "python.disableInstallationCheck": true, >> settings.json
	echo     "python.linting.pylintEnabled": true, >> settings.json
	echo     "python.venvPath": "U:\\virtual_envs" >> settings.json
	echo } >> settings.json
	cd ..
)
:: creating template files
echo.> README.md
IF "%new_git_repo%" == "y" (
	:: git publish
	git init
	git add README.md
	git commit -m "first commit - [make workspace script]"
	git remote add origin git@github.com:yvovonBerg/%name%.git
	start "" https://github.com/new
)
