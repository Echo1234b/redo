@echo off
echo ========================================
echo  Bitcoin Analyzer - Windows Setup
echo ========================================
echo.

echo [1/6] Checking Python installation...
py --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
echo ✅ Python is installed

echo.
echo [2/6] Upgrading pip...
py -m pip install --upgrade pip

echo.
echo [3/6] Installing core dependencies...
py -m pip install streamlit pandas numpy plotly scikit-learn

echo.
echo [4/6] Installing Windows-specific packages...
py -m pip install pywin32 wmi

echo.
echo [5/6] Installing MetaTrader5...
py -m pip install MetaTrader5
if errorlevel 1 (
    echo ⚠️  MetaTrader5 installation failed - app will run in demo mode
) else (
    echo ✅ MetaTrader5 installed successfully
)

echo.
echo [6/6] Installing TA-Lib...

REM Get Python version for wheel selection
for /f "tokens=2" %%i in ('py --version 2^>^&1') do set PYTHON_VERSION=%%i
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do set PYTHON_MAJOR=%%a& set PYTHON_MINOR=%%b

echo Detected Python %PYTHON_VERSION%

REM Try multiple TA-Lib installation methods
echo Method 1: Trying pip install with wheel...
py -m pip install TA-Lib
if not errorlevel 1 (
    echo ✅ TA-Lib installed successfully via pip
    goto :setup_complete
)

echo Method 2: Trying with specific wheel repository...
py -m pip install --index-url https://pypi.org/simple/ TA-Lib
if not errorlevel 1 (
    echo ✅ TA-Lib installed successfully via PyPI
    goto :setup_complete
)

echo Method 3: Trying with Christoph Gohlke's repository...
py -m pip install --index-url https://pypi.anaconda.org/cgohlke/simple/ TA-Lib
if not errorlevel 1 (
    echo ✅ TA-Lib installed successfully via Christoph Gohlke's repository
    goto :setup_complete
)

echo Method 4: Trying to download and install wheel directly...
echo Downloading TA-Lib wheel for Python %PYTHON_MAJOR%.%PYTHON_MINOR%...

REM Create temp directory for download
if not exist "%TEMP%\ta-lib-install" mkdir "%TEMP%\ta-lib-install"
cd /d "%TEMP%\ta-lib-install"

REM Try to download appropriate wheel
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.lfd.uci.edu/~gohlke/pythonlibs/TA_Lib-0.4.24-cp%PYTHON_MAJOR%%PYTHON_MINOR%-cp%PYTHON_MAJOR%%PYTHON_MINOR%-win_amd64.whl' -OutFile 'TA_Lib.whl'}" 2>nul
if exist "TA_Lib.whl" (
    py -m pip install TA_Lib.whl
    if not errorlevel 1 (
        echo ✅ TA-Lib installed successfully via downloaded wheel
        cd /d /workspace
        goto :setup_complete
    )
)

REM If all methods failed, try conda as last resort
echo Method 5: Trying conda installation...
conda install -c conda-forge ta-lib -y
if not errorlevel 1 (
    echo ✅ TA-Lib installed successfully via conda
    cd /d /workspace
    goto :setup_complete
)

echo.
echo ❌ All TA-Lib installation methods failed
echo.
echo 💡 To fix this issue, please try one of the following:
echo.
echo 1. Install Visual C++ Build Tools:
echo    - Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
echo    - Install "C++ build tools" workload
echo    - Restart your computer and run this script again
echo.
echo 2. Install TA-Lib manually:
echo    - Download wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/
echo    - Choose: TA_Lib-0.4.24-cp%PYTHON_MAJOR%%PYTHON_MINOR%-cp%PYTHON_MAJOR%%PYTHON_MINOR%-win_amd64.whl
echo    - Install with: pip install [downloaded-file].whl
echo.
echo 3. Use conda environment:
echo    - Install Anaconda/Miniconda
echo    - Run: conda install -c conda-forge ta-lib
echo.
echo The application will run with basic indicators only.
cd /d /workspace

:setup_complete
echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo To run the application:
echo   1. Open MetaTrader 5 terminal (if available)
echo   2. Run: python run_app.py
echo   3. Open http://localhost:8501 in your browser
echo.
echo For MT5 integration:
echo   - Make sure MT5 terminal is running
echo   - Enable "Allow DLL imports" in MT5 settings
echo   - Use your MT5 login credentials in the app
echo.
pause
