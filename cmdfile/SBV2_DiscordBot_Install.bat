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



%CURL% -L -o %GIT_NAME% %GIT_URL%
%GIT_NAME% -y
del %GIT_NAME%
set GIT=PortableGit\bin\git.exe
%GIT% clone https://github.com/p2-3r/Discord-ReadTextBot-for-Style-Bert-VITS2-API.git


%CURL% -L -o %FMP_NAME% %FMP_URL%
%POWERSHELL% Expand-Archive -Path %FMP_NAME%
del %FMP_NAME%


%CURL% -L -o %PYTHON_ZIPNAME% %PYTHON_URL%
%POWERSHELL% Expand-Archive -Path %PYTHON_ZIPNAME%
del %PYTHON_ZIPNAME%
%POWERSHELL% "&{(Get-Content -Path '%PYTHON_DIR%/python310._pth') -creplace '#import site', 'import site' | Set-Content -Path '%PYTHON_DIR%/python310._pth'}"\


%CURL% -L -o %PYTHON_DIR%/get-pip.py https://bootstrap.pypa.io/get-pip.py
%PYTHON% %PYTHON_DIR%/get-pip.py --no-warn-script-location
%PYTHON% -m pip install virtualenv --no-warn-script-location
set temp_=%ERRORLEVEL%

pause
