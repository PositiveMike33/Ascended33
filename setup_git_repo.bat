@echo off
cd /d D:\Vault\Vault

echo Setting up Git repository...
C:\PROGRA~1\Git\cmd\git.exe config --global user.name "Vault Manager" 2>nul || C:\PROGRA~1\Git\cmd\git.exe config user.name "Vault Manager"
C:\PROGRA~1\Git\cmd\git.exe config --global user.email "vault@local" 2>nul || C:\PROGRA~1\Git\cmd\git.exe config user.email "vault@local"

echo Adding files...
C:\PROGRA~1\Git\cmd\git.exe add .

echo Committing...
C:\PROGRA~1\Git\cmd\git.exe commit -m "vault: cleanup duplicates and optimize structure (53MB freed)"

echo Done!
C:\PROGRA~1\Git\cmd\git.exe log --oneline -5

pause
