@echo off
cd /d "%~dp0"

echo Creating virtual environment...
python -m venv venv
echo Setting up virtual environment...
call "venv\Scripts\activate.bat"

echo Upgrading pip...
pip install --upgrade pip
echo Installing required packages...
pip install -r requirements.txt

SET /P ocrspace_api_key="Enter your OCR.space API key: "
echo Saving API key to config.py...
echo "ocrspace_api_key = '%ocrspace_api_key%'" > config.py

echo Setup complete. You can now run the application using app.bat.
pause