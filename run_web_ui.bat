@echo off
REM Task Automation Suite - Web Server Startup (Windows)

echo.
echo ======================================================
echo  Task Automation Suite - Web UI
echo  One-Click Task Creation Interface
echo ======================================================
echo.

REM Check if .env exists
if not exist .env (
    echo Error: .env file not found!
    echo.
    echo Please create .env file with your credentials:
    echo   copy .env.example .env
    echo   (edit .env with your actual credentials)
    echo.
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Install Playwright
echo Installing Playwright browsers...
python -m playwright install chromium

echo.
echo ======================================================
echo  Setup Complete!
echo ======================================================
echo.
echo Opening browser...
echo.
echo Web UI: http://localhost:5000
echo.
start http://localhost:5000

REM Run the server
python web_server.py

pause
