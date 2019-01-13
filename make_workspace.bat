@echo off
set /p root="Enter root path: (D:\workspace\repos)" || SET "root=D:\workspace\repos"
set /p name="Enter project name: "
set /p new_git_repo="Make new git repo [y/n]: "
set /p is_python="Python project: [y/n]: "
set /p new_venv="Make new virtual env: [y/n]: "
set full_path="%root%\%name%"

IF NOT EXIST %full_path% ( mkdir %full_path% )
cd /D "%full_path%"
:: python stuff
IF "%is_python%" == "y" (
        IF "%new_venv%" == "y" ( 
			virtualenv D:\VENV\%name%
		)
	mkdir .vscode
	cd .vscode
	echo.> settings.json
	echo { > settings.json
	echo     "python.linting.enabled": true, >> settings.json
	echo     "python.pythonPath": "D:\\VENV\\%name%\\Scripts\\python.exe", >> settings.json
	echo     "python.disableInstallationCheck": true, >> settings.json
	echo     "python.linting.pylintEnabled": true, >> settings.json
	echo     "python.venvPath": "D:\\VENV", >> settings.json
	echo     "python.linting.flake8Enabled": false >> settings.json
	echo } >> settings.json
	cd ..
	D:/VENV/%name%/Scripts/python.exe -m pip install -U "pylint<2.0.0"
)
python append_project.py %name% %full_path%
:: creating template files
echo.> README.md
IF "%new_git_repo%" == "y" (
	:: git publish
	git init
	git add README.md
	git commit -m "first commit"
	git remote add origin git@github.com:yvovonberg/%name%.git
	start "" https://github.com/new
)