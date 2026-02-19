@echo off
setlocal enabledelayedexpansion

:: ================================================================
:: ASCENDED33 LAUNCHER - Docker Edition
:: Kali + hexstrike + Tor tournent dans des conteneurs Docker.
:: Aucun chemin hardcode - portable sur toutes les machines.
:: ================================================================

:: Chemin du repo = dossier de ce .bat
set REPO_PATH=%~dp0
set REPO_PATH=!REPO_PATH:~0,-1!

:: ================================================================
:: CONFIG LOCALE (gitignored) — charge config/local.bat si present
:: Copier config/local.bat.example -> config/local.bat et editer
:: ================================================================
if exist "!REPO_PATH!\config\local.bat" call "!REPO_PATH!\config\local.bat"

:: Obsidian vault (defaut D:\Vault si non defini dans local.bat)
if "!OBSIDIAN_VAULT_PATH!"=="" set OBSIDIAN_VAULT_PATH=D:\Vault

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

:: ================================================================
::  BANNIERE
:: ================================================================
echo.
echo  +==========================================+
echo  ^|                                          ^|
echo  ^|       ASCENDED33  WORKSPACE              ^|
echo  ^|  Docker  ^|  Tor  ^|  hexstrike  ^|  Obsidian  ^|
echo  ^|                                          ^|
echo  +==========================================+
echo.

:: ================================================================
:: STEP 1 — Docker containers (Tor + Kali + hexstrike)
:: ================================================================
call :start_docker

:: ================================================================
:: STEP 2 — Obsidian
:: ================================================================
call :open_obsidian

:: ================================================================
:: STEP 3 — Dashboard Streamlit
:: ================================================================
call :launch_dashboard

:: ================================================================
:: RESUME FINAL — statut reel de chaque service
:: ================================================================
echo.
echo  +==========================================+
echo  ^|   ASCENDED33 WORKSPACE                   ^|
echo  +------------------------------------------+

:: Dashboard Streamlit
netstat -ano 2>nul | findstr ":8501" >nul 2>&1
if not errorlevel 1 (
    echo  ^|  [OK] Dashboard  : http://localhost:8501  ^|
) else (
    echo  ^|  [--] Dashboard  : non demarre           ^|
)

:: hexstrike-ai (port 8888 mappe depuis le conteneur)
if "!HEXSTRIKE_OK!"=="1" (
    echo  ^|  [OK] hexstrike  : http://localhost:8888  ^|
) else (
    echo  ^|  [--] hexstrike  : non confirme           ^|
)

:: Tor (anonymisation)
if "!TOR_OK!"=="1" (
    echo  ^|  [OK] Tor        : trafic anonymise        ^|
) else (
    echo  ^|  [--] Tor        : bootstrap en cours     ^|
)

:: Kali
docker inspect --format "{{.State.Status}}" ascended33_kali 2>nul | findstr "running" >nul 2>&1
if not errorlevel 1 (
    echo  ^|  [OK] Kali       : ascended33_kali         ^|
) else (
    echo  ^|  [--] Kali       : non demarre            ^|
)

:: Obsidian
tasklist 2>nul | findstr /I "Obsidian.exe" >nul 2>&1
if not errorlevel 1 (
    echo  ^|  [OK] Obsidian   : Vault ouvert           ^|
) else (
    echo  ^|  [--] Obsidian   : non detecte            ^|
)

:: REST API Obsidian
curl -s -o nul -w "%%{http_code}" http://localhost:27123/ 2>nul | findstr /R "^[24]" >nul 2>&1
if not errorlevel 1 (
    echo  ^|  [OK] REST API   : http://localhost:27123 ^|
) else (
    echo  ^|  [--] REST API   : plugin non active      ^|
)

echo  +==========================================+
echo.
echo  Commandes utiles :
echo    docker compose ps                   (etat des conteneurs)
echo    docker compose logs -f tor          (bootstrap Tor)
echo    docker compose exec kali bash       (shell Kali)
echo    docker compose restart tor          (nouveau circuit Tor)
echo.
pause
exit /b 0


:: ================================================================
:start_docker
:: Demarre les conteneurs Docker (Tor + Kali + hexstrike)
:: ================================================================
echo [1/3] Docker containers (Tor + Kali + hexstrike)...

:: Docker disponible ?
where docker >nul 2>&1
if errorlevel 1 (
    echo  [ERREUR] docker non trouve dans PATH.
    echo  Installez Docker Desktop : https://www.docker.com/products/docker-desktop/
    exit /b 1
)

:: docker-compose.yml present ?
if not exist "!REPO_PATH!\docker-compose.yml" (
    echo  [WARN] docker-compose.yml introuvable dans !REPO_PATH!
    echo  Ce fichier doit exister a la racine du repo.
    exit /b 0
)

:: Demarrer les conteneurs en arriere-plan
echo  Demarrage des conteneurs...
docker compose -f "!REPO_PATH!\docker-compose.yml" up -d --remove-orphans
if errorlevel 1 (
    echo  [WARN] docker compose up a echoue. Voir les messages ci-dessus.
    echo  Verifier : docker compose -f "!REPO_PATH!\docker-compose.yml" logs
    exit /b 0
)
echo  [OK] Conteneurs lances.

:: Attendre hexstrike sur localhost:8888 (max 60s = 30 essais x 2s)
echo  Attente hexstrike-ai sur localhost:8888 (max 60s)...
set /a _hex_tries=0
:_docker_hex_check
set /a _hex_tries+=1
if %_hex_tries% GTR 30 (
    echo  [WARN] hexstrike-ai ne repond pas apres 60s.
    echo  Verifier : docker compose -f "!REPO_PATH!\docker-compose.yml" logs hexstrike
    set HEXSTRIKE_OK=0
    exit /b 0
)
curl -s -o nul -w "%%{http_code}" http://localhost:8888/ 2>nul | findstr /R "^[24]" >nul 2>&1
if errorlevel 1 (
    timeout /t 2 /nobreak >nul
    goto :_docker_hex_check
)
set HEXSTRIKE_OK=1
echo  [OK] hexstrike-ai : http://localhost:8888

:: Statut Tor (healthy = circuit etabli, starting = bootstrap en cours)
for /f %%i in ('docker inspect --format "{{.State.Health.Status}}" ascended33_tor 2^>nul') do set TOR_STATUS=%%i
if "!TOR_STATUS!"=="healthy" (
    echo  [OK] Tor : circuit actif — trafic hexstrike + Kali anonymise
    set TOR_OK=1
) else (
    echo  [INFO] Tor : bootstrap en cours (~30s). Le trafic sera anonymise sous peu.
    set TOR_OK=0
)

exit /b 0


:: ================================================================
:open_obsidian
:: ================================================================
echo [2/3] Obsidian Vault...

if not exist "!OBSIDIAN_EXE!" (
    echo  [WARN] Obsidian introuvable. Lance setup.ps1 pour l installer.
    exit /b 0
)

:: Verifier que le vault existe
if not exist "!OBSIDIAN_VAULT_PATH!" (
    echo  [WARN] Vault introuvable : !OBSIDIAN_VAULT_PATH!
    echo  Verifie OBSIDIAN_VAULT_PATH dans config\local.bat
    echo  Lancement Obsidian sans vault specifique...
    start "" "!OBSIDIAN_EXE!"
    exit /b 0
)

:: Obsidian deja ouvert ?
tasklist | findstr /I "Obsidian.exe" >nul 2>&1
if not errorlevel 1 (
    echo  [OK] Obsidian deja ouvert ^(Vault: !OBSIDIAN_VAULT_PATH!^).
    exit /b 0
)

:: Ouvrir Obsidian sur le vault specifique
start "" "!OBSIDIAN_EXE!" "!OBSIDIAN_VAULT_PATH!"
echo  [OK] Obsidian lance sur : !OBSIDIAN_VAULT_PATH!

:: Attendre 5s pour que le plugin Local REST API s initialise (port 27123)
echo  Attente initialisation plugin REST API Obsidian...
timeout /t 5 /nobreak >nul

:: Verifier si la REST API repond
curl -s -o nul -w "%%{http_code}" http://localhost:27123/ 2>nul | findstr /R "^[24]" >nul 2>&1
if not errorlevel 1 (
    echo  [OK] Obsidian REST API active ^(port 27123^).
) else (
    echo  [INFO] REST API non detectee — normal si plugin pas encore configure.
    echo  Pour l activer : Obsidian ^> Parametres ^> Community plugins ^> Local REST API
)
exit /b 0


:: ================================================================
:launch_dashboard
:: ================================================================
echo [3/3] Dashboard Ascended33...

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
