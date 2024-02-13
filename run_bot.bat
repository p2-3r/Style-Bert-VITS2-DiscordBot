@echo off

if not exist "./venv/Scripts/activate" (
    echo [34mINFO[0m^|[32m%time:~0,2%:%time:~3,2%:%time:~6,2%[0m^|Preparing to launch the bot...
    python -m venv venv
    call "./venv/Scripts/activate"
    echo [34mINFO[0m^|[32m%time:~0,2%:%time:~3,2%:%time:~6,2%[0m^|Preparing to launch the bot...
    echo [34mINFO[0m^|[32m%time:~0,2%:%time:~3,2%:%time:~6,2%[0m^|Installing requirements.txt...
    pip install -r requirements.txt
    echo [33mCOMPLETE[0m^|[32m%time:~0,2%:%time:~3,2%:%time:~6,2%[0m^|Library installation is complete.
) else (
    call "./venv/Scripts/activate"
)

echo [34mINFO[0m^|[32m%time:~0,2%:%time:~3,2%:%time:~6,2%[0m^|Running the bot...
python ./src/main.py
