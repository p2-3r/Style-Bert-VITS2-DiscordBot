@echo off

echo [34mINFO[0m^|[32m%time:~0,2%:%time:~3,2%:%time:~6,2%[0m^|Running update...

git clone --quiet https://github.com/p2-3r/Discord-ReadTextBot-for-Style-Bert-VITS2-API

if exist "Discord-ReadTextBot-for-Style-Bert-VITS2-API" (

    cd Discord-ReadTextBot-for-Style-Bert-VITS2-API

    if exist ".git" (

        rd /S /Q .git

    )

    cd ..
)

python update.py