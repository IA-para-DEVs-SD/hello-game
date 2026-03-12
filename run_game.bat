@echo off
cd /d "%~dp0"
set PYTHONPATH=%CD%\src;%PYTHONPATH%
.venv\Scripts\python.exe -c "import pygame; pygame.init(); print('PyGame OK')"
if errorlevel 1 (
    echo ERRO: PyGame nao esta funcionando corretamente
    pause
    exit /b 1
)
.venv\Scripts\python.exe src\pyblaze\main.py
pause
