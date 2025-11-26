@echo off
setlocal enabledelayedexpansion

echo Suche nach Dateien: GHC_*.py
echo.

:: Liste aller passenden Dateien einlesen
set count=0
for %%f in (GHC_*.py) do (
    set /a count+=1
    set "file[!count!]=%%f"
    echo !count!: %%f
)

:: Prüfen, ob Dateien gefunden wurden
if %count%==0 (
    echo Keine passenden Dateien gefunden!
    pause
    exit /b
)

echo.
set /p choice="Bitte Nummer eingeben: "

:: Prüfen, ob die Eingabe gültig ist
if not defined file[%choice%] (
    echo Ungültige Auswahl!
    pause
    exit /b
)

set "selected=!file[%choice%]!"
echo.
echo Starte Datei: %selected%
echo.
cls
python "%selected%"

pause