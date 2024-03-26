@echo off
cd %~dp0
chcp 65001 > NUL

if not exist "./venv/Scripts/activate" (
    echo [34mINFO[0m^|起動準備中...
    python -m venv venv
    call "./venv/Scripts/activate"
    echo [34mINFO[0m^|起動準備中...
    echo [34mINFO[0m^|必要なライブラリをダウンロードしています...
    pip install -r requirements.txt
    echo [33mCOMPLETE[0m^|ライブラリのインストールが完了しました。
) else (
    call "./venv/Scripts/activate"
)

echo [34mINFO[0m^|Running the bot...
python main.py

pause