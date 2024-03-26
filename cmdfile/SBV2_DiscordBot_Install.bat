@echo off
chcp 65001 > NUL
cd %~dp0

set POWERSHELL=PowerShell -ExecutionPolicy Bypass

set GIT_URL=https://github.com/git-for-windows/git/releases/download/v2.25.1.windows.1/PortableGit-2.25.1-64-bit.7z.exe
set GIT_NAME=PortableGit-2.25.1-64-bit.7z.exe
set CURL=C:\Windows\System32\curl.exe

set FMP_URL=https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip
set FMP_NAME=ffmpeg-master-latest-win64-gpl.zip 

set PYTHON_URL=https://www.python.org/ftp/python/3.10.11/python-3.10.11-embed-amd64.zip
set PYTHON_DIR=python-3.10.11-embed-amd64
set PYTHON_ZIPNAME=python-3.10.11-embed-amd64.zip
set PYTHON="python-3.10.11-embed-amd64/python.exe"


echo [34mINFO[0m^|Downloading GIT...
%CURL% -L -o %GIT_NAME% %GIT_URL%

echo [34mINFO[0m^|Unzip Git...
%GIT_NAME% -y
del %GIT_NAME%
set GIT=PortableGit\bin\git.exe

echo [34mINFO[0m^|Downloading BOT program...
%GIT% clone -b dev https://github.com/p2-3r/Style-Bert-VITS2-DiscordBot.git

echo [34mINFO[0m^|Downloading ffmpeg...
%CURL% -L -o %FMP_NAME% %FMP_URL%
%POWERSHELL% Expand-Archive -Path %FMP_NAME%
del %FMP_NAME%

echo [34mINFO[0m^|Downloading Python...
%CURL% -L -o %PYTHON_ZIPNAME% %PYTHON_URL%
%POWERSHELL% Expand-Archive -Path %PYTHON_ZIPNAME%
del %PYTHON_ZIPNAME%
%POWERSHELL% "&{(Get-Content -Path '%PYTHON_DIR%/python310._pth') -creplace '#import site', 'import site' | Set-Content -Path '%PYTHON_DIR%/python310._pth'}"\

%CURL% -L -o %PYTHON_DIR%/get-pip.py https://bootstrap.pypa.io/get-pip.py
%PYTHON% %PYTHON_DIR%/get-pip.py --no-warn-script-location
%PYTHON% -m pip install virtualenv --no-warn-script-location
set temp_=%ERRORLEVEL%

move /y PortableGit "Style-Bert-VITS2-DiscordBot/downloads/PortableGit"
move /y ffmpeg-master-latest-win64-gpl "Style-Bert-VITS2-DiscordBot/downloads/ffmpeg-master-latest-win64-gpl"
move /y %PYTHON_DIR% "Style-Bert-VITS2-DiscordBot/downloads/%PYTHON_DIR%"
set temp_=%ERRORLEVEL%

echo [33mCOMPLETE[0m^|Download is complete. To start, please launch bot_start.bat.
pause

del "%~f0"