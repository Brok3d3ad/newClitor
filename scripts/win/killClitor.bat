@echo off
:: Check if PID is provided
if "%~1"=="" (
    echo Usage: %0 ^<PID^>
    exit /b 1
)

:: Kill the process using the provided PID
taskkill /PID %1 /F
