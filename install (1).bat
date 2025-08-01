@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Define download URLs
set "PYTHON_URL=https://www.python.org/ftp/python/3.13.5/python-3.13.5-amd64.exe"
set "GIT_URL=https://github.com/git-for-windows/git/releases/download/v2.45.1.windows.1/Git-2.45.1-64-bit.exe"

:: Define filenames
set "PYTHON_EXE=python-3.13.5-amd64.exe"
set "GIT_EXE=Git-2.45.1-64-bit.exe"

:: Create a temp folder
set "TEMP_DIR=%TEMP%\setup_env"
mkdir "%TEMP_DIR%"
cd /d "%TEMP_DIR%"

echo =============================================
echo Downloading Python 3.13.5 installer...
echo =============================================
curl -L -o %PYTHON_EXE% %PYTHON_URL%
if errorlevel 1 (
    echo Failed to download Python installer.
    pause
    exit /b 1
)

echo Installing Python 3.13.5...
start /wait %PYTHON_EXE% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
if errorlevel 1 (
    echo Python installation failed.
    pause
    exit /b 1
)

echo =============================================
echo Downloading Git installer...
echo =============================================
curl -L -o %GIT_EXE% %GIT_URL%
if errorlevel 1 (
    echo Failed to download Git installer.
    pause
    exit /b 1
)

echo Installing Git...
start /wait %GIT_EXE% /VERYSILENT
if errorlevel 1 (
    echo Git installation failed.
    pause
    exit /b 1
)

:: Refresh environment variables
echo Refreshing environment...
set "PATH=%ProgramFiles%\Git\bin;%ProgramFiles%\Git\cmd;%PATH%"

:: Check Python and pip
where python >nul 2>&1 || (
    echo Python not found in PATH. Please restart your PC or add Python to PATH manually.
    pause
    exit /b 1
)

:: Upgrade pip and install packages
echo =============================================
echo Installing Python dependencies...
echo =============================================

python -m pip install --upgrade pip

python -m pip install ^
  discord ^
  datetime 

if errorlevel 1 (
    echo Some packages failed to install.
    pause
    exit /b 1
)

echo.
echo ✅ Setup complete! Python 3.13.5, Git, and all dependencies installed.
pause
ENDLOCAL
