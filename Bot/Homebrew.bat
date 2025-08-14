
::
::YAwzoRdxOk+EWAnk
::fBw5plQjdG8=
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSzk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+IeA==
::cxY6rQJ7JhzQF1fEqQJgZko0
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQIUIQhXQxaGfEm1EvU5+/v+4f6Oo0EONA==
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATE0Uw0LQlYRQqHfFiuE7EV5/ub
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCyDJGyX8VAjFDp3aTa+GGStCLkT6ezo086OsU4SRuZ/WoDPmpGdM+Ud/kzleYUR/nVXnckeCQwYKEbrTAYguiBHrmHl
::YB416Ek+ZW8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
net session >nul 2>nul
if %errorlevel% neq 0 (
    echo Not running as an administrator.
    echo Trying to restart the script as an administrator...
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit
)
chcp 437>nul
chcp 65001 >nul
mode con cols=140 lines=49
title Discord Bot Essentials - Enderline
cls
cd /d "%~dp0"
for /f %%a in ('"cd"') do set Location=%%a

:variables
set version=0.5
set g=[92m
set r=[91m
set red=[04m
set l=[1m
set w=[0m
set b=[94m
set m=[95m
set p=[35m
set c=[35m
set d=[96m
set u=[0m
set z=[91m
set n=[96m
set y=[40;33m
set g2=[102m
set r2=[101m
set t=[40m

:cut1
cls
echo.
echo %b% Developed by : %p%Enderline
timeout /t 2 >nul
%g%
goto cut3

:cut3
goto cut4

:cut4
cls
echo.
echo -- Discord Bot Essentials! --
echo  Application Version : 0.5 By  %p%Enderline
timeout /t 4 >nul
cls

:menu
%g%
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
set /p opcao=Choose an option (1-8): 

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
cls
goto menu

:latest
%w%
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
cls
goto menu

:pip
%w%
echo Installing bot dependencies via PowerShell...

powershell -Command "python -m pip install --upgrade pip"

powershell -Command "python -m pip install discord.py"

powershell -Command "python -m pip install python-dotenv"

echo All dependencies have been installed!
pause
cls
goto menu

:config
cls
echo %w%=============================
echo            %r%Token%w%
echo =============================
echo. %n%
set /p token=Enter the bot token:

echo DISCORD_TOKEN=%token%> .env

echo.
echo Token configured!
pause
cls
goto menu

:startip
%w%
cls
(
  echo @echo off
  echo cd /d C:\Bot\
  echo py -3 main.py
  echo pause
) > Startup.bat
echo Arquivo Startup.bat criado com sucesso!
pause
cls
goto menu

:edit
%w%
notepad main.py
cls
goto menu

:github
%w%
start https://github.com/Enderline164/Discord-Bot-Essentials
echo.
timeout /t 2 >nul
goto menu

:start
%g%
cls
echo %w%=============================
echo     %r%Starting the Bot...%w%
echo =============================

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
