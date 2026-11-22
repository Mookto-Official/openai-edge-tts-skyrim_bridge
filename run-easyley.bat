@echo off
cd /d "%~dp0"
call venv\Scripts\activate
python skyrim_bridge.py
pause