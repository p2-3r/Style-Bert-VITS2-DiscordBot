@echo off

echo running update...

git clone https://github.com/p2-3r/Discord-ReadTextBot-for-Style-Bert-VITS2-API

cd Discord-ReadTextBot-for-Style-Bert-VITS2-API
rd /S /Q .git

cd ..

python update.py