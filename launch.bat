@echo off
echo Starting Tetris...

if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
    
    echo Activating virtual environment and installing dependencies...
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

cd src
python tetris.py

echo Game ended.
pause
