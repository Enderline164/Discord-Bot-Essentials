@echo off
net session >nul 2>nul
if %errorlevel% neq 0 (
    echo Not running as an administrator.
    echo Trying to restart the script as an administrator...
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit
)

chcp 437 >nul
chcp 65001 >nul
mode con cols=140 lines=49
title Discord Bot Essentials - Enderline
cls
cd /d "%~dp0"

:variables
set "version=0.5"
set "g=[92m"
set "r=[91m"
set "red=[04m"
set "l=[1m"
set "w=[0m"
set "b=[94m"
set "m=[95m"
set "p=[35m"
set "c=[35m"
set "d=[96m"
set "u=[0m"
set "z=[91m"
set "n=[96m"
set "y=[40;33m"
set "g2=[102m"
set "r2=[101m"
set "t=[40m"

:cut1
cls
echo.
echo %b% Developed by : %p%Enderline
timeout /t 2 >nul
goto cut4

:cut4
cls
echo.
echo -- Discord Bot Essentials! --
echo  Application Version : %version% By %p%Enderline
timeout /t 4 >nul

:menu %g%
cls
echo %w%=============================%w%
echo    %b%Discord Bot Essentials%g%
echo        %w%By Enderline%g%
echo %w%=============================%w%
echo. %n%
echo [1] Token
echo [2] Start
echo [3] Create Startup
echo [4] Github
echo [5] Edit Main.py
echo [6] Install Latest Version
echo [7] Install Bot Dependencies
echo [8] Credits
echo [9] Exit
echo.
set /p "opcao=Choose an option (1-9): "

if "%opcao%"=="1" goto config
if "%opcao%"=="2" goto start
if "%opcao%"=="3" goto startip
if "%opcao%"=="4" goto github
if "%opcao%"=="5" goto edit
if "%opcao%"=="6" goto latest
if "%opcao%"=="7" goto pip
if "%opcao%"=="8" goto credits
if "%opcao%"=="9" goto fim

echo.
echo Invalid option. Please try again.
timeout /t 2 >nul
goto menu

:credits
cls
echo %w%=============================%w%
echo    %b%Discord Bot Essentials%g%
echo          %c%Credits%g%
echo %w%=============================%w%
echo.
echo %c% Enderline - Developer and creator of the Discord Bot Essentials
echo.
echo %d% KillDev - Discord Bot Essentials Logo%w%
echo.
pause
goto menu

:latest %w%
echo Creating folder Latest...
mkdir Latest 2>nul

echo Downloading repository zip...
curl -L -o repo.zip https://github.com/Enderline164/Discord-Bot-Essentials/archive/refs/heads/main.zip

echo Extracting Bot folder...
powershell -Command "Expand-Archive -Path 'repo.zip' -DestinationPath '.' -Force"

echo Moving files to Latest...
xcopy "Discord-Bot-Essentials-main\Bot" "Latest" /E /I /Y

echo Cleaning up...
rd /S /Q "Discord-Bot-Essentials-main"
del repo.zip

echo Done! All files are now in the Latest folder.
pause
goto menu

:pip %w%
echo Installing bot dependencies via PowerShell...

powershell -Command "python -m pip install --upgrade pip"
powershell -Command "python -m pip install discord.py"
powershell -Command "python -m pip install python-dotenv"

echo All dependencies have been installed!
pause
goto menu

:config
cls
echo %w%=============================
echo            %r%Token%w%
echo ==============================
echo. %n%
set /p "token=Enter the bot token: "

echo DISCORD_TOKEN=%token%> .env

echo.
echo Token configured!
pause
goto menu

:startip %w%
cls
(
  echo @echo off
  echo cd /d C:\Bot\
  echo py -3 main.py
  echo pause
) > Startup.bat
echo Startup.bat created successfully!
pause
goto menu

:edit %w%
notepad main.py
goto menu

:github %w%
start https://github.com/Enderline164/Discord-Bot-Essentials
timeout /t 2 >nul
goto menu

:start %g%
cls
echo %w%=============================
echo     %r%Starting the Bot...%w%
echo ==============================

if exist ".env" (
    for /f "tokens=2 delims==" %%A in ('findstr "DISCORD_TOKEN=" .env') do (
        echo Using token: %%A
    )
) else (
    echo File .env not found. Configure the token first!
    pause
    goto menu
)

cd /d "C:\Bot\"
py -3 main.py

echo.
echo The bot has been terminated.
pause
goto menu

:fim
cls
echo Closing...
timeout /t 1 >nul
exit