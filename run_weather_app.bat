@echo off

echo Starting batch file at %date% %time% >> batch_log.txt
cd /d %~dp0
echo Changed directory to: %cd% >> batch_log.txt

echo Activating virtual environment >> batch_log.txt
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment >> batch_log.txt
    exit /b 1
)
echo Virtual environment activated >> batch_log.txt

echo Running Python script >> batch_log.txt
python scheduler.py >> python_log.txt 2>&1
set PYTHON_EXIT_CODE=%errorlevel%
echo Python script completed with exit code %PYTHON_EXIT_CODE% >> batch_log.txt
type python_log.txt >> batch_log.txt

echo Deactivating virtual environment >> batch_log.txt >> batch_log.txt
call deactivate

echo Batch file execution complete at %date% %time% >> batch_log.txt

exit /b %PYTHON_EXIT_CODE%