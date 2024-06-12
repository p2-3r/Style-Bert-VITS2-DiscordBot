@echo off
cd %~dp0
chcp 65001 > NUL

if exist "downloads/python-3.10.11-embed-amd64/python.exe" (
    set PYTHON_PATH="downloads/python-3.10.11-embed-amd64/python.exe"
) else (
    set PYTHON_PATH="python"
)

if %PYTHON_PATH%=="python" (

    if not exist "./venv/Scripts/activate" (
        echo [34mINFO[0m^|Preparing to launch...
        %PYTHON_PATH% -m venv venv
        call "./venv/Scripts/activate"
        echo [34mINFO[0m^|Downloading libraries...
        pip install uv
        uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
        uv pip install -r requirements.txt
    ) else (
        call "./venv/Scripts/activate"
    )

) else (
    if not exist "./venv/Scripts/activate" (

        %PYTHON_PATH% -m virtualenv --copies venv

        echo [34mINFO[0m^|Preparing to launch...
        call "./venv/Scripts/activate"

        echo [34mINFO[0m^|Downloading libraries...
        pip install uv
        uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
        uv pip install -r requirements.txt
    ) else (
        call "./venv/Scripts/activate"
    )

)

echo [34mINFO[0m^|Running the bot...
python main.py

pause