@echo off
REM Ascended33 Project Launcher - Batch Wrapper
REM This script activates the entire Ascended33 project with services, VS Code, and Streamlit

setlocal enabledelayedexpansion

cd /d "D:\Vault\Vault\Ascended33"

REM Launch PowerShell script with elevation if needed
powershell -NoProfile -ExecutionPolicy Bypass -Command "& 'D:\Vault\Vault\Ascended33\LAUNCH_ASCENDED33.ps1'"

pause
