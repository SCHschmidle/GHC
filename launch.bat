@echo off
setlocal enabledelayedexpansion
:loop:
cls
python "ghc/main.py"
pause
GOTO loop