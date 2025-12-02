import warnings
warnings.filterwarnings("ignore")
import re
from datetime import datetime, timedelta
import requests
import urllib3
import os
from GHC_OCR import save_clipboard_image, OCR_clipboard_image, delete_clipboard_image


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# User-spezifische Einstellungen
user = None
try:
    user = os.getlogin()
except Exception:
    user = None

if user == "carcane" or user == "carcanne":
    target_location = "Rotkreuz"
    walking_time = timedelta(minutes=7)
    minus_time = timedelta(minutes=20)
elif user == "schmidle" or user == "albissre":
    target_location = "Hellbühl"
    walking_time = timedelta(minutes=5)
    minus_time = timedelta(minutes=20)
else:
    # Default
    target_location = "Rotkreuz"
    walking_time = timedelta(minutes=7)
    minus_time = timedelta(minutes=20)
target = timedelta(hours=8)
pause = timedelta()
lunch_time = timedelta(minutes=30)
i = 0


# Styling
ascii_art = r"""                                                               
  _______   ______      __    __    ______    ___  ___   _______      ______     ___       __        ______ 
 /  _____| /  __  \    |  |  |  |  /  __  \  |   \/   | |   ____|    /      |   /   \     |  |      /      |
|  |  __  |  |  |  |   |  |__|  | |  |  |  | |  \  /  | |  |__      |  ,----'  /  ^  \    |  |     |  ,----'
|  | |_ | |  |  |  |   |   __   | |  |  |  | |  |\/|  | |   __|     |  |      /  /_\  \   |  |     |  |     
|  |__| | |  `--'  |   |  |  |  | |  `--'  | |  |  |  | |  |____    |  `----./  _____  \  |  `----.|  `----.
 \______|  \______/ [_]|__|  |__|  \______/  |__|  |__| |_______|[_] \______/__/     \__\ |_______| \______|
                                                                                                             
 -   ____________ ____________ ____________ 7 ____________ ____________ 7 ____________ ____________ ____________
--  / #  #  #  # ¦ #  #  #  # ¦ #  #  #  # ¦¨¦ #  #  #  # ¦ #  #  #  # ¦¨¦ #  #  #  # ¦ #  #  #  # ¦ #  #  #  # \\
 -- °°¨¨¨¨¨¨¨¨¨¨¨°¨¨¨¨¨¨¨¨¨¨¨¨°¨¨¨¨¨¨¨¨¨¨¨¨°°°¨¨¨¨¨¨¨¨¨¨¨¨°¨¨¨¨¨¨¨¨¨¨¨¨°°°¨¨¨¨¨¨¨¨¨¨¨¨°¨¨¨¨¨¨¨¨¨¨¨¨°¨¨¨¨¨¨¨¨¨¨¨°°
"""
print("\033[0;94m" + ascii_art + "\033[0m")
print("------------------------------------------------------------------------------------------------------------------ \n \n")

# Auswahl: Text oder OCR
print("Text oder OCR")
decision = input("Gib '1' für Text oder '2' für OCR ein: ")
print()


if decision == '1':
    text = input("Gib mir deine TimeTool Zeiten: ")
    print()
    zeiten = re.findall(r'\d{1,2}:\d{2}', text)
    for zeit in zeiten:
        zeiten[i] = datetime.strptime(zeit, "%H:%M") # Start nach lunch
        i += 1
elif decision == '2':
    save_clipboard_image()
    text, zeiten = OCR_clipboard_image()
    delete_clipboard_image()

    if len(zeiten) < 3:
        print("Nicht genügend Zeiten im Bild gefunden. Bitte stelle sicher, dass das Bild drei Zeiten enthält.")
        exit()
    # Annahme: OCR gibt Zeiten in umgekehrter Reihenfolge zurück
    #zeiten = zeiten[::-1]  
    zeiten = [datetime.strptime(zeit, "%H:%M") for zeit in zeiten]  
    
    
else:
    print("Ungültige Eingabe. Bitte starte das Programm neu und gib '1' oder '2' ein.")
    exit()


# Differenz berechnen
i=2
# Lunch time berechnen
pause = timedelta()
for j in range(1, len(zeiten)-1, 2):
    pause += zeiten[j+1] - zeiten[j]

if pause > lunch_time:
    lunch_time = pause

end_time = zeiten[-1] + target + lunch_time
print(f"Du musst bis \033[31m{end_time.strftime('%H:%M')}\033[0m arbeiten")

# Verbindungen abfragen
r = requests.get(
    f"https://transport.opendata.ch/v1/connections?from=Buchrain&to={target_location}&time={(end_time + walking_time - minus_time).strftime('%H:%M')}&limit=6",
    verify=False
)
data = r.json()
print()
print("Nächste Abfahrten ab Buchrain:")
for verbindung in data.get("connections", []):
    abfahrt = datetime.fromisoformat(verbindung["from"]["departure"])
    print(f"  {abfahrt.strftime('%H:%M')} Uhr")

# Optional: Zahlen als ASCII-Art für schmidle
numbers_art = [
[
"                    ",
"      00000000      ",
"    000      000    ",
"   000        000   ",
"  000          000  ",
"  000          000  ",
"  000          000  ",
"   000        000   ",
"    000      000    ",
"      00000000      ",
"                    ",
],
[
"                    ",
"      00000         ",
"    000  00         ",
"  000    00         ",
"         00         ",
"         00         ",
"         00         ",
"         00         ",
"         00         ",
"         00         ",
"                    ",
],
[
"                    ",
"      000000        ",
"    000    0000     ",
"  000        000    ",
"             000    ",
"           000      ",
"         000        ",
"       000          ",
"     000            ",
"   0000000000000    ",
"                    ",
],
[
"                    ",
"     0000000000     ",
"             0000   ",
"              00    ",
"              000   ",
"     0000000000     ",
"              000   ",
"              000   ",
"             0000   ",
"     0000000000     ",
"                    ",
],
[
"                    ",
"      000000        ",
"     000 000        ",
"    000  000        ",
"   000   000        ",
"  000000000000000   ",
"         000        ",
"         000        ",
"         000        ",
"         000        ",
"                    ",
],
[
"                    ",
"  00000000000000    ",
"  000               ",
"  000               ",
"  0000000000000     ",
"            00000   ",
"              000   ",
"             0000   ",
"           00000    ",
"  000000000000      ",
"                    ",
],
[
"                    ",
"      000           ",
"     000            ",
"    000             ",
"   000 000000       ",
"  000000   00000    ",
"  0000       0000   ",
"  000         000   ",
"   0000     0000    ",
"      00000000      ",
"                    ",
],
[
"                    ",
"    000000000000    ",
"            000     ",
"           000      ",
"          000       ",
"    000000000000    ",
"        000         ",
"       000          ",
"      000           ",
"     000            ",
"                    ",
],
[
"                    ",
"      00000000      ",
"    000      000    ",
"   000        000   ",
"    000      000    ",
"     0000000000     ",
"    000      000    ",
"   000         000  ",
"    000       000   ",
"      00000000      ",
"                    ",
],
[
"                    ",
"      00000000      ",
"    000      000    ",
"   000        000   ",
"    000      000    ",
"      000000000     ",
"           000      ",
"           000      ",
"          000       ",
"         000        ",
"                    ",
]
]


if user == "schmidle":
    x = re.findall(r"\d", end_time.strftime("%H%M"))
    print("\033[0;94m")
    for i in range(11):
        for digit in x:
            digit = int(digit)
            print(numbers_art[digit][i], end="")
        print()