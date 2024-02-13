@echo off

FOR /F "usebackq" %%i IN (`powershell -Command "$json = Get-Content -Path data.json | ConvertFrom-Json;return $json.settings.style_bertvits2_path"`) DO SET PATH=%%i

cd %PATH%

if exist "./venv/Scripts/activate" (
    call "./venv/Scripts/activate"
) else (
    echo [31mERROR[0m: Could not start Style-Bert-VITS2 venv
    pause
    exit
)

if exist "server_fastapi.py" (
    echo [34mINFO[0m^|[32m%time:~0,2%:%time:~3,2%:%time:~6,2%[0m^|Running server_fastapi.py...
    python server_fastapi.py
) else (
    echo [31mERROR[0m: Not found server_fastapi.py
    pause
    exit
)
