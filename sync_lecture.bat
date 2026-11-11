@echo off
setlocal enabledelayedexpansion

:: Lecture Material Sync Utility
:: Fetches selected date folder from upstream and pushes to origin/main

echo ========================================================
echo   Lecture Material Sync Utility (Upstream to Origin)
echo ========================================================

:: 1. Fetch latest commits from upstream
echo [*] Fetching latest commits from upstream...
git fetch upstream
if errorlevel 1 (
    echo [ERROR] Failed to fetch from upstream. Check network or remote.
    pause
    exit /b 1
)

:: 2. Determine target date folder
set TARGET_DATE=%1
if "%TARGET_DATE%"=="" (
    set /p TARGET_DATE="Enter date folder to download (e.g. 20261111): "
)

if "%TARGET_DATE%"=="" (
    echo [ERROR] Target date folder name cannot be empty.
    pause
    exit /b 1
)

echo [*] Target folder: %TARGET_DATE%

:: 3. Checkout the target folder from upstream/main
echo [*] Extracting %TARGET_DATE% from upstream/main...
git checkout upstream/main -- %TARGET_DATE%
if errorlevel 1 (
    echo [ERROR] Folder '%TARGET_DATE%' not found in upstream/main.
    pause
    exit /b 1
)

:: 4. Commit and push to origin/main
echo [*] Staging and committing %TARGET_DATE%...
git add %TARGET_DATE%
git commit -m "feat: %TARGET_DATE% lecture material auto sync"
echo [*] Pushing to origin/main...
git push origin main
if errorlevel 1 (
    echo [ERROR] Failed to push to origin/main.
    pause
    exit /b 1
)

echo ========================================================
echo [SUCCESS] %TARGET_DATE% successfully synced and pushed!
echo ========================================================
pause
