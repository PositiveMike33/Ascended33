@echo off
setlocal enabledelayedexpansion

:: ================================================================
:: ASCENDED33 LAUNCHER - Portable (aucun chemin hardcode)
:: Le script detecte automatiquement tous les chemins
:: ================================================================

:: Chemin du repo = dossier de ce .bat (fonctionne sur n importe quelle machine)
set REPO_PATH=%~dp0
set REPO_PATH=!REPO_PATH:~0,-1!

:: ================================================================
:: CONFIG LOCALE (gitignored) — charge config/local.bat si present
:: Copier config/local.bat.example vers config/local.bat et editer
:: ================================================================
if exist "!REPO_PATH!\config\local.bat" call "!REPO_PATH!\config\local.bat"

:: Kali VM (valeurs par defaut si non definies dans local.bat)
:: KALI_IP intentionnellement vide si non defini — le launcher gere gracieusement
if "!KALI_USER!"=="" set KALI_USER=kali

:: Chemin vers le .vmx Kali (si vide = auto-detection dans :find_vmx)
:: Ne pas modifier ici — definir dans config\local.bat a la place

:: ================================================================
:: DETECTION AUTOMATIQUE DES OUTILS
:: ================================================================

:: Python - cherche dans les emplacements courants
set PYTHON=%USERPROFILE%\AppData\Local\Programs\Python\Python313\python.exe
if not exist "!PYTHON!" set PYTHON=%USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe
if not exist "!PYTHON!" set PYTHON=%USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe
if not exist "!PYTHON!" (
    for /f "delims=" %%p in ('where python 2^>nul') do (
        set PYTHON=%%p
        goto :python_set
    )
)
:python_set

:: Obsidian
set OBSIDIAN_EXE=%USERPROFILE%\AppData\Local\Obsidian\Obsidian.exe

:: VMware vmrun (x86 ou x64)
set VMRUN=C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe
if not exist "!VMRUN!" set VMRUN=C:\Program Files\VMware\VMware Workstation\vmrun.exe

:: Cle SSH Kali : d abord dans ~/.ssh, sinon sur le disque (config\ssh\)
set KALI_KEY=%USERPROFILE%\.ssh\kali_lab_key
if not exist "!KALI_KEY!" set KALI_KEY=!REPO_PATH!\config\ssh\kali_lab_key

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
echo  ^|  Obsidian   : Vault                      ^|
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

:: KALI_IP doit etre defini dans config\local.bat
if "!KALI_IP!"=="" (
    echo  [WARN] KALI_IP non defini. Copier config\local.bat.example vers config\local.bat et configurer.
    exit /b 0
)

:: VM deja reachable ?
ping -n 1 -w 1000 %KALI_IP% >nul 2>&1
if not errorlevel 1 (
    echo  [OK] Kali VM deja en ligne ^(%KALI_IP%^).
    exit /b 0
)

:: vmrun disponible ?
if not exist "!VMRUN!" (
    echo  [WARN] vmrun introuvable. Lance la VM manuellement depuis VMware.
    exit /b 0
)

:: Auto-detection VMX si vide
if "!KALI_VMX!"=="" (
    echo  Recherche fichier .vmx Kali...
    call :find_vmx
)

:: VMX trouvable ?
if "!KALI_VMX!"=="" (
    echo  [WARN] Aucun fichier .vmx Kali trouve automatiquement.
    echo  Definis KALI_VMX dans ce script.
    exit /b 0
)
if not exist "!KALI_VMX!" (
    echo  [WARN] VMX introuvable : !KALI_VMX!
    exit /b 0
)

:: Lancer la VM
echo  Demarrage Kali VM...
"!VMRUN!" -T ws start "!KALI_VMX!"
echo  [OK] Kali VM demarree.
exit /b 0


:: ================================================================
:find_vmx
:: Cherche un .vmx contenant "kali" dans les emplacements courants
:: ================================================================
set _VMX_DIRS=%USERPROFILE%\Documents\Virtual Machines
set _VMX_DIRS2=%USERPROFILE%\Virtual Machines
set _VMX_DIRS3=%USERPROFILE%\Downloads
set _VMX_DIRS4=D:\Virtual Machines
set _VMX_DIRS5=D:\VMs
set _VMX_DIRS6=C:\VMs

for %%d in ("%_VMX_DIRS%" "%_VMX_DIRS2%" "%_VMX_DIRS3%" "%_VMX_DIRS4%" "%_VMX_DIRS5%" "%_VMX_DIRS6%") do (
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
ssh -i "%KALI_KEY%" -o StrictHostKeyChecking=accept-new -o ConnectTimeout=2 -o BatchMode=yes %KALI_USER%@%KALI_IP% "exit" >nul 2>&1
if errorlevel 1 (
    timeout /t 2 /nobreak >nul
    goto :_ssh_loop
)

:: hexstrike deja running ?
for /f %%i in ('ssh -i "%KALI_KEY%" -o StrictHostKeyChecking^=accept-new -o BatchMode^=yes %KALI_USER%@%KALI_IP% "pgrep -f hexstrike_server.py > /dev/null 2>&1 && echo 1 || echo 0" 2^>nul') do set HEX_STATUS=%%i
if "%HEX_STATUS%"=="1" (
    echo  [OK] hexstrike-ai deja en cours.
    exit /b 0
)

:: Lancer hexstrike
ssh -i "%KALI_KEY%" -o StrictHostKeyChecking=accept-new -o BatchMode=yes %KALI_USER%@%KALI_IP% "cd ~/hexstrike-ai && source hexstrike-env/bin/activate && nohup python3 hexstrike_server.py > ~/hexstrike.log 2>&1 &" >nul 2>&1
echo  [OK] hexstrike-ai demarre ^(port 8888^).
exit /b 0


:: ================================================================
:open_obsidian
:: ================================================================
echo [3/4] Obsidian Vault...

if not exist "!OBSIDIAN_EXE!" (
    echo  [WARN] Obsidian introuvable. Lance setup.ps1 pour l installer.
    exit /b 0
)

:: Obsidian deja ouvert ?
tasklist | findstr /I "Obsidian.exe" >nul 2>&1
if not errorlevel 1 (
    echo  [OK] Obsidian deja ouvert.
    exit /b 0
)

start "" "!OBSIDIAN_EXE!"
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
if not exist "!PYTHON!" (
    echo  [ERREUR] Python introuvable. Lance setup.ps1 pour l installer.
    exit /b 1
)

cd /d "!REPO_PATH!"
start /B "" "!PYTHON!" -m streamlit run streamlit_app.py --server.headless false --server.port 8501 > "!REPO_PATH!\streamlit.log" 2>&1

:_streamlit_wait
timeout /t 2 /nobreak >nul
netstat -ano | findstr ":8501" >nul 2>&1
if errorlevel 1 goto :_streamlit_wait

start http://localhost:8501
echo  [OK] Dashboard : http://localhost:8501
exit /b 0
