@echo off
set /p root="Enter root path: (D:\workspace\repos)" || SET "root=D:\workspace\repos"
set /p name="Enter project name: "
set /p git_link="Enter git link: "
set /p is_python="Python project: [y/n]: "
set /p new_venv="Make new virtual env: [y/n]: "
set full_path="%root%\%name%"

cd /D %root%
git clone %git_link%
cd /D %full_path%

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
	IF EXIST %full_path%\requirements.txt (
		D:/VENV/%name%/Scripts/python.exe -m pip install -r %full_path%\requirements.txt
	)
	
)
python "U:\tools\internal\workflowtools\append_project.py" %name% %full_path%