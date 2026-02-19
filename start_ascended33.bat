@echo off
title Ascended33 — Launching...
color 0A

echo.
echo  ██████████████████████████████████████
echo  █                                    █
echo  █        ASCENDED33 LAUNCHER         █
echo  █                                    █
echo  ██████████████████████████████████████
echo.

:: --- Chemin vers le repo (modifie si necessaire) ---
set REPO_PATH=D:\Vault\Vault\Ascended33
set PYTHON=C:\Users\th3th\AppData\Local\Programs\Python\Python313\python.exe

:: --- Verifier que Python existe ---
%PYTHON% --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python introuvable. Verifiez votre installation.
    pause
    exit /b 1
)

:: --- Verifier si Streamlit est deja en cours ---
netstat -ano | findstr ":8501" >nul 2>&1
if not errorlevel 1 (
    echo [OK] Streamlit deja en cours sur http://localhost:8501
    goto open_browser
)

:: --- Lancer Streamlit en arriere-plan ---
echo [1/3] Demarrage Streamlit...
cd /d "%REPO_PATH%"
start /B "" %PYTHON% -m streamlit run streamlit_app.py --server.headless false --server.port 8501 >"%REPO_PATH%\streamlit.log" 2>&1

:: --- Attendre que Streamlit soit pret ---
echo [2/3] Attente demarrage...
:wait_loop
timeout /t 2 /nobreak >nul
netstat -ano | findstr ":8501" >nul 2>&1
if errorlevel 1 goto wait_loop

:open_browser
:: --- Ouvrir le dashboard dans le browser ---
echo [3/3] Ouverture dashboard...
start http://localhost:8501

echo.
echo  [OK] Ascended33 Dashboard : http://localhost:8501
echo  [OK] Streamlit tourne en arriere-plan
echo  [OK] Logs : %REPO_PATH%\streamlit.log
echo.
echo  Ferme cette fenetre quand tu as fini de travailler.
echo  (Streamlit continuera en arriere-plan)
echo.
pause
