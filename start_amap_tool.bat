@echo off
chcp 65001 >nul
echo Starting Amap Tool...
echo.

cd /d "%~dp0"

REM Check if uv is installed
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: uv package manager not found
    echo Please install uv first: https://docs.astral.sh/uv/getting-started/installation/
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    uv venv
    if %errorlevel% neq 0 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Install/update dependencies
echo Installing/updating dependencies...
uv pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

REM Start application
echo Starting application...
uv run python main.py

if %errorlevel% neq 0 (
    echo Application failed to start
    pause
)