@echo off
TITLE Job Hunter AI - Launching...

:: 1. Verifiy if python is install
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] Python nis not installed in PATH.
    echo Please install python from python.org (Choose "Add to PATH").
    pause
    exit
)

:: 2. Check if venv exists, or create it
IF NOT EXIST "venv" (
    echo [INSTALLATION] First launch detected, creation of the environment...
    python -m venv venv
    echo [INSTALLATION] Libraries installation...
    call venv\Scripts\activate
    pip install -r requirements.txt
    echo [OK] Installation is done !
) ELSE (
    call venv\Scripts\activate
)

:: 3. Luanch Streamlit interface
echo.
echo Launching interface...
echo Don't close this winodw while you're using the interface.
echo.
streamlit run gui.py

pause