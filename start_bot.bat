@echo off
echo ========================================
echo   GoalBuddy21 - Telegram Bot
echo ========================================
echo.

cd /d "%~dp0"

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting bot...
echo.
python run.py

pause

