@echo off
title Ascended33 — Initialisation...
color 0A

:: ================================================================
:: CONFIGURATION — Verifie et adapte ces chemins a ton systeme
:: ================================================================

set REPO_PATH=D:\Vault\Vault\Ascended33
set PYTHON=C:\Users\th3th\AppData\Local\Programs\Python\Python313\python.exe
set KALI_IP=192.168.157.128
set KALI_USER=kali
set KALI_KEY=C:\Users\th3th\.ssh\kali_lab_key
set OBSIDIAN_EXE=C:\Users\th3th\AppData\Local\Obsidian\Obsidian.exe
set VMRUN=C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe

:: Laisser vide = auto-detection (recherche *.vmx contenant "kali")
:: Ou forcer manuellement : set KALI_VMX=C:\chemin\vers\kali.vmx
set KALI_VMX=

:: ================================================================
::  BANNIERE
:: ================================================================
echo.
echo  +==========================================+
echo  ^|                                          ^|
echo  ^|       ASCENDED33  WORKSPACE              ^|
echo  ^|   Kali  ^|  HexStrike  ^|  Obsidian        ^|
echo  ^|                                          ^|
echo  +==========================================+
echo.

:: ================================================================
:: STEP 1 — VMware + Kali VM
:: ================================================================
call :launch_vm

:: ================================================================
:: STEP 2 — Attente SSH + hexstrike-ai
:: ================================================================
call :start_hexstrike

:: ================================================================
:: STEP 3 — Obsidian
:: ================================================================
call :open_obsidian

:: ================================================================
:: STEP 4 — Dashboard Streamlit
:: ================================================================
call :launch_dashboard

:: ================================================================
:: RESUME FINAL
:: ================================================================
echo.
echo  +==========================================+
echo  ^|   ASCENDED33 OPERATIONNEL                ^|
echo  +------------------------------------------+
echo  ^|  Dashboard  : http://localhost:8501      ^|
echo  ^|  HexStrike  : http://%KALI_IP%:8888     ^|
echo  ^|  Obsidian   : D:\Vault                   ^|
echo  +==========================================+
echo.
echo  Ferme cette fenetre quand tu as fini.
echo.
pause
exit /b 0


:: ================================================================
:launch_vm
:: ================================================================
echo [1/4] VMware / Kali Linux...

:: VM deja reachable ?
ping -n 1 -w 1000 %KALI_IP% >nul 2>&1
if not errorlevel 1 (
    echo  [OK] Kali VM deja en ligne ^(%KALI_IP%^).
    exit /b 0
)

:: vmrun disponible ?
if not exist "%VMRUN%" (
    echo  [WARN] vmrun introuvable : %VMRUN%
    echo  Lance la VM manuellement depuis VMware.
    exit /b 0
)

:: Auto-detection VMX si non defini
if "%KALI_VMX%"=="" (
    echo  Recherche fichier .vmx Kali...
    call :find_vmx
)

:: VMX trouvable ?
if "%KALI_VMX%"=="" (
    echo  [WARN] Aucun fichier .vmx Kali trouve automatiquement.
    echo  Definis KALI_VMX manuellement dans ce script.
    exit /b 0
)
if not exist "%KALI_VMX%" (
    echo  [WARN] VMX introuvable : %KALI_VMX%
    exit /b 0
)

:: Lancer la VM
echo  Demarrage Kali VM : %KALI_VMX%
"%VMRUN%" -T ws start "%KALI_VMX%"
echo  [OK] Kali VM demarree.
exit /b 0


:: ================================================================
:find_vmx
:: Cherche un .vmx contenant "kali" dans les emplacements courants
:: ================================================================
set _VMX_DIRS=%USERPROFILE%\Documents\Virtual Machines
set _VMX_DIRS2=%USERPROFILE%\Virtual Machines
set _VMX_DIRS3=D:\Virtual Machines
set _VMX_DIRS4=D:\VMs
set _VMX_DIRS5=C:\VMs

for %%d in ("%_VMX_DIRS%" "%_VMX_DIRS2%" "%_VMX_DIRS3%" "%_VMX_DIRS4%" "%_VMX_DIRS5%") do (
    if exist %%d (
        for /f "delims=" %%f in ('dir /s /b %%d\*.vmx 2^>nul ^| findstr /I "kali"') do (
            set KALI_VMX=%%f
            echo  [OK] VMX trouve : %%f
            exit /b 0
        )
    )
)
exit /b 0


:: ================================================================
:start_hexstrike
:: ================================================================
echo [2/4] hexstrike-ai sur Kali %KALI_IP%...

:: Attendre SSH (max 90s = 45 essais x 2s)
set /a _tries=0
:_ssh_loop
set /a _tries+=1
if %_tries% GTR 45 (
    echo  [WARN] SSH timeout apres 90s. hexstrike-ai non demarre.
    exit /b 0
)
ssh -i "%KALI_KEY%" -o StrictHostKeyChecking=no -o ConnectTimeout=2 -o BatchMode=yes %KALI_USER%@%KALI_IP% "exit" >nul 2>&1
if errorlevel 1 (
    timeout /t 2 /nobreak >nul
    goto :_ssh_loop
)

:: hexstrike deja running ?
for /f %%i in ('ssh -i "%KALI_KEY%" -o StrictHostKeyChecking^=no -o BatchMode^=yes %KALI_USER%@%KALI_IP% "pgrep -f hexstrike_server.py > /dev/null 2>&1 && echo 1 || echo 0" 2^>nul') do set HEX_STATUS=%%i
if "%HEX_STATUS%"=="1" (
    echo  [OK] hexstrike-ai deja en cours.
    exit /b 0
)

:: Lancer hexstrike
ssh -i "%KALI_KEY%" -o StrictHostKeyChecking=no -o BatchMode=yes %KALI_USER%@%KALI_IP% "cd ~/hexstrike-ai && source hexstrike-env/bin/activate && nohup python3 hexstrike_server.py > ~/hexstrike.log 2>&1 &" >nul 2>&1
echo  [OK] hexstrike-ai demarre ^(port 8888^).
exit /b 0


:: ================================================================
:open_obsidian
:: ================================================================
echo [3/4] Obsidian Vault...

if not exist "%OBSIDIAN_EXE%" (
    echo  [WARN] Obsidian introuvable : %OBSIDIAN_EXE%
    exit /b 0
)

:: Obsidian deja ouvert ?
tasklist | findstr /I "Obsidian.exe" >nul 2>&1
if not errorlevel 1 (
    echo  [OK] Obsidian deja ouvert.
    exit /b 0
)

start "" "%OBSIDIAN_EXE%"
echo  [OK] Obsidian lance.
exit /b 0


:: ================================================================
:launch_dashboard
:: ================================================================
echo [4/4] Dashboard Ascended33...

:: Streamlit deja running ?
netstat -ano | findstr ":8501" >nul 2>&1
if not errorlevel 1 (
    echo  [OK] Dashboard deja en cours sur http://localhost:8501
    start http://localhost:8501
    exit /b 0
)

:: Python disponible ?
"%PYTHON%" --version >nul 2>&1
if errorlevel 1 (
    echo  [ERREUR] Python introuvable : %PYTHON%
    exit /b 1
)

cd /d "%REPO_PATH%"
start /B "" "%PYTHON%" -m streamlit run streamlit_app.py --server.headless false --server.port 8501 > "%REPO_PATH%\streamlit.log" 2>&1

:_streamlit_wait
timeout /t 2 /nobreak >nul
netstat -ano | findstr ":8501" >nul 2>&1
if errorlevel 1 goto :_streamlit_wait

start http://localhost:8501
echo  [OK] Dashboard : http://localhost:8501
exit /b 0
