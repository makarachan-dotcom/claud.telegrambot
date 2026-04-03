@echo off
chcp 65001 >nul

:: AI STAND WY2.5 - Startup Script for Windows
:: Created by Kimi K2.5

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║  🤖 AI STAND WY2.5 - Telegram Bot                           ║
echo ║                                                              ║
echo ║  Starting up...                                              ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo 📦 Activating virtual environment...
    call venv\Scripts\activate.bat
)

:: Check if .env exists
if not exist ".env" (
    echo ⚠️  Warning: .env file not found!
    echo    Please copy .env.example to .env and configure your bot token.
    echo.
    echo    copy .env.example .env
    echo    notepad .env  :: Edit and add your token
    echo.
    pause
    exit /b 1
)

:: Load environment variables
for /f "tokens=*" %%a in (.env) do (
    set %%a
)

if "%TELEGRAM_BOT_TOKEN%"=="" (
    echo ❌ Error: TELEGRAM_BOT_TOKEN not set!
    echo    Please add your bot token to the .env file.
    pause
    exit /b 1
)

:: Create necessary directories
echo 📁 Creating directories...
if not exist "data" mkdir data
if not exist "sessions" mkdir sessions

:: Run the bot
echo.
echo 🚀 Starting bot...
echo    Press Ctrl+C to stop
echo.

python run.py

pause
