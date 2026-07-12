#!/bin/bash

echo "Starting Tetris..."

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    
    echo "Activating virtual environment and installing dependencies..."
    source .venv/bin/activate
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

cd src
python3 tetris.py

echo "Game ended."
