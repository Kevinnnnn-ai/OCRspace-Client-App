@echo off
cd /d "%~dp0"

echo Activating virtual environment...
call "venv\Scripts\activate.bat"

echo Running app...
python "src\gui.py"