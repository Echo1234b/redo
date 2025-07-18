@echo off
echo ========================================
echo  Bitcoin Analyzer - Windows Setup
echo ========================================
echo.

echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
echo ✅ Python is installed

echo.
echo [2/5] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [3/5] Installing core dependencies...
python -m pip install streamlit pandas numpy plotly scikit-learn

echo.
echo [4/5] Installing Windows-specific packages...
python -m pip install pywin32 wmi

echo.
echo [5/5] Installing MetaTrader5 and TA-Lib...

REM Try to install MetaTrader5
echo Installing MetaTrader5...
python -m pip install MetaTrader5
if errorlevel 1 (
    echo ⚠️  MetaTrader5 installation failed - app will run in demo mode
) else (
    echo ✅ MetaTrader5 installed successfully
)

REM Try to install TA-Lib
echo Installing TA-Lib...
python -m pip install --find-links=https://github.com/mrjbq7/ta-lib/releases/latest --prefer-binary TA-Lib
if errorlevel 1 (
    echo ⚠️  TA-Lib installation failed - using basic indicators
    echo 💡 You may need to install Visual C++ Build Tools
    echo    Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
) else (
    echo ✅ TA-Lib installed successfully
)

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