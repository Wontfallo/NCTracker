@echo off
echo ========================================
echo   NCTracker - Quality NCR System
echo   Starting Application...
echo ========================================
echo.

echo [1/3] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo [2/3] Installing/Updating dependencies...
pip install -r requirements.txt

echo [3/3] Starting NCTracker application...
echo.
echo NCTracker will open in your default browser
echo Default login: admin / admin123
echo Press Ctrl+C to stop the application
echo.
echo ========================================
streamlit run Home.py