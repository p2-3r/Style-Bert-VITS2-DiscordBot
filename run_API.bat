@echo off

FOR /F "usebackq" %%i IN (`powershell -Command "$json = Get-Content -Path data.json | ConvertFrom-Json;return $json.settings.style_bertvits2_path"`) DO SET PATH=%%i

cd %PATH%

if exist "./venv/Scripts/activate" (
    call "./venv/Scripts/activate"
) else (
    echo ERROR: Could not start Style-Bert-VITS2 venv
    pause
    exit
)

if exist "server_fastapi.py" (
    echo Running server_fastapi.py...
    python server_fastapi.py
) else (
    echo ERROR: Not found server_fastapi.py
    pause
    exit
)
