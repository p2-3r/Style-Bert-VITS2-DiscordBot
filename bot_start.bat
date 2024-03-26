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
        echo [34mINFO[0m^|起動準備中...
        %PYTHON_PATH% -m venv venv
        call "./venv/Scripts/activate"
        echo [34mINFO[0m^|必要なライブラリをダウンロードしています...
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
        pip install -r requirements.txt
        echo [33mCOMPLETE[0m^|ライブラリのインストールが完了しました。
    ) else (
        call "./venv/Scripts/activate"
    )

) else (
    if not exist "./venv/Scripts/activate" (

        %PYTHON_PATH% -m virtualenv --copies venv

        echo [34mINFO[0m^|起動準備中...
        call "./venv/Scripts/activate"

        echo [34mINFO[0m^|必要なライブラリをダウンロードしています...
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
        pip install -r requirements.txt
        echo [33mCOMPLETE[0m^|ライブラリのインストールが完了しました。
    ) else (
        call "./venv/Scripts/activate"
    )

)

echo [34mINFO[0m^|Running the bot...
python main.py

pause