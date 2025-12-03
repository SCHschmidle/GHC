import warnings
warnings.filterwarnings("ignore")
import re
from datetime import datetime, timedelta
import requests
import urllib3
import os
from OCR import save_clipboard_image, OCR_clipboard_image, delete_clipboard_image
from main import *


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
zeiten = get_times(2)
save_clipboard_image()
if return_value := save_clipboard_image() == False:
    print("Keine Bilddaten in der Zwischenablage gefunden. Bitte stelle sicher, dass du einen Screenshot in die Zwischenablage kopiert hast.")
    exit()
text, zeiten = OCR_clipboard_image()
delete_clipboard_image()

    
zeiten = [datetime.strptime(zeit, "%H:%M") for zeit in zeiten]  
    

# Differenz berechnen
i=2
# Lunch time berechnen
pause = timedelta()
for j in range(1, len(zeiten)-1, 2):
    pause += zeiten[j-1] - zeiten[j]

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

