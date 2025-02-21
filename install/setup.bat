@echo off

:: Check if Python is installed
python --version > NUL 2>&1
if errorlevel 1 goto NoPython

:RunInstaller
python ./installer.py
goto :Finish

:NoPython
echo This installer requires Python.
echo No Python installation found...
set /p UserInput=Do you want to install Python 3.11 now (Y/N)?
if /i "%UserInput%"=="Y" goto :StartPythonInstaller

echo Please visit https://www.python.org and install Python then rerun this installer.
goto :Finish

:StartPythonInstaller
python-3.11.4-amd64.exe
goto :RunInstaller

:Finish
pause