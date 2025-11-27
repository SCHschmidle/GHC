import warnings
warnings.filterwarnings("ignore")
import re
from datetime import datetime, timedelta
import requests
import urllib3
import os

try:
    import easyocr
except ImportError:
    easyocr = None

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
elif user == "schmidle" or user == "albissre":
    target_location = "Hellbühl"
    walking_time = timedelta(minutes=5)
else:
    # Default
    target_location = "Rotkreuz"
    walking_time = timedelta(minutes=7)

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
if easyocr is not None:
    print("Text oder OCR")
    decision = input("Gib '1' für Text oder '2' für OCR ein: ")
    print()
else:
    decision = '1'

if decision == '1':
    text = input("Gib mir deine TimeTool Zeiten: ")
    print()
    zeiten = re.findall(r'\d{1,2}:\d{2}', text)
    if len(zeiten) < 3:
        print("Nicht genügend Zeiten gefunden. Bitte gib mindestens drei Zeiten im Format HH:MM ein.")
        exit()
    zeit1 = zeiten[0]
    zeit2 = zeiten[1]
    zeit3 = zeiten[2]
elif decision == '2' and easyocr is not None:
    path = input("Gib den Pfad zum Bild ein: ")
    reader = easyocr.Reader(["de"])
    text = reader.readtext(path, detail=0)
    text = " ".join(text)
    text = re.sub(r'(\d{1,2})\.(\d{2})', r'\1:\2', text)
    print(text)
    zeiten = re.findall(r'\d{1,2}:\d{2}', text)
    if len(zeiten) < 3:
        print("Nicht genügend Zeiten im Bild gefunden. Bitte stelle sicher, dass das Bild drei Zeiten enthält.")
        exit()
    # Annahme: OCR gibt Zeiten in umgekehrter Reihenfolge zurück
    zeit1 = zeiten[2]
    zeit2 = zeiten[1]
    zeit3 = zeiten[0]
else:
    print("Ungültige Eingabe. Bitte starte das Programm neu und gib '1' oder '2' ein.")
    exit()

# In datetime-Objekte konvertieren
t1 = datetime.strptime(zeit1, "%H:%M") # Start after lunch
t2 = datetime.strptime(zeit2, "%H:%M") # End before lunch
t3 = datetime.strptime(zeit3, "%H:%M") # Start morning
target = timedelta(hours=8)

# Differenz berechnen
differenz = t2 - t3
print(f"Du hast \033[32m{differenz}\033[0m gearbeitet")

if (t1-t2 < timedelta(minutes=30)):
    t1 = t2 + timedelta(minutes=30)
end_time = t1 + target - differenz
print(f"Du musst bis \033[31m{end_time.strftime('%H:%M')}\033[0m arbeiten")

# Verbindungen abfragen
r = requests.get(
    f"https://transport.opendata.ch/v1/connections?from=Buchrain&to={target_location}&time={(end_time + walking_time).strftime('%H:%M')}&limit=4",
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
    "00000000000000000000",
    "000000        000000",
    "0000   000000   0000",
    "000   00000000   000",
    "00   0000000000   00",
    "00   0000000000   00",
    "00   0000000000   00",
    "00   0000000000   00",
    "000   00000000   000",
    "0000   000000   0000",
    "000000        000000",
    "00000000000000000000"
    ],
    [
    "00000000000000000000",
    "000000     000000000",
    "0000   00  000000000",
    "00   0000  000000000",
    "000000000  000000000",
    "000000000  000000000",
    "000000000  000000000",
    "000000000  000000000",
    "000000000  000000000",
    "000000000  000000000",
    "00000000000000000000"
    ],
    [
    "00000000000000000000",
    "000000      00000000",
    "0000   0000    00000",
    "00   00000000   0000",
    "0000000000000   0000",
    "00000000000   000000",
    "000000000   00000000",
    "0000000   0000000000",
    "00000   000000000000",
    "000             0000",
    "00000000000000000000"
    ],

    [
    "00000000000000000000",
    "00000          00000",
    "0000000000000    000",
    "00000000000000  0000",
    "00000000000000   000",
    "00000          00000",
    "00000000000000   000",
    "00000000000000   000",
    "0000000000000    000",
    "00000          00000",
    "00000000000000000000"
    ],
    [
    "00000000000000000000",
    "000000      00000000",
    "00000   0   00000000",
    "0000   00   00000000",
    "000   000   00000000",
    "00               000",
    "000000000   00000000",
    "000000000   00000000",
    "000000000   00000000",
    "000000000   00000000",
    "00000000000000000000"
    ],
    [
    "00000000000000000000",
    "00              0000",
    "00   000000000000000",
    "00   000000000000000",
    "00             00000",
    "000000000000     000",
    "00000000000000   000",
    "0000000000000    000",
    "00000000000     0000",
    "00            000000",
    "00000000000000000000"
    ],
    [
    "00000000000000000000",
    "000000   00000000000",
    "00000   000000000000",
    "0000   0000000000000",
    "000   0      0000000",
    "00      000     0000",
    "00    0000000    000",
    "00   000000000   000",
    "000    00000    0000",
    "000000        000000",
    "00000000000000000000"
    ],
    [
    "00000000000000000000",
    "0000            0000",
    "000000000000   00000",
    "00000000000   000000",
    "0000000000   0000000",
    "0000            0000",
    "00000000   000000000",
    "0000000   0000000000",
    "000000   00000000000",
    "00000   000000000000",
    "00000000000000000000"
    ],

    [
    "00000000000000000000",
    "000000        000000",
    "0000   000000   0000",
    "000   00000000   000",
    "0000   000000   0000",
    "00000          00000",
    "0000   000000   0000",
    "000   000000000   00",
    "0000   0000000   000",
    "000000        000000",
    "00000000000000000000"
    ],
    [
    "00000000000000000000",
    "000000        000000",
    "0000   000000   0000",
    "000   00000000   000",
    "0000   000000   0000",
    "000000         00000",
    "00000000000   000000",
    "00000000000   000000",
    "0000000000   0000000",
    "000000000   00000000",
    "00000000000000000000"
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