@echo off

if not exist "./venv/Scripts/activate" (
    echo Preparing to launch the bot...
    python -m venv venv
    call "./venv/Scripts/activate"
    pip install -r requirements.txt
) else (
    call "./venv/Scripts/activate"
)

echo Running the bot...
python ./src/main.py
