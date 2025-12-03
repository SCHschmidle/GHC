import warnings
warnings.filterwarnings("ignore")
import re
from datetime import datetime, timedelta
import requests
import urllib3
import os
from OCR import save_clipboard_image, OCR_clipboard_image, delete_clipboard_image
import pandas as pd
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



# Functions
def get_times(decision):
    i=0
    if decision == '1':
        text = input("Gib mir deine TimeTool Zeiten: ")
        print()
        zeiten = re.findall(r'\d{1,2}:\d{2}', text)
        for zeit in zeiten:
            zeiten[i] = datetime.strptime(zeit, "%H:%M") # Start nach lunch
            i += 1
        return zeiten
    elif decision == '2':
        save_clipboard_image()
        if not save_clipboard_image():
            print("Keine Bilddaten in der Zwischenablage gefunden. Bitte stelle sicher, dass du einen Screenshot in die Zwischenablage kopiert hast.")
            exit()
        text, zeiten = OCR_clipboard_image(path="clipboard_screenshot.png")
        delete_clipboard_image()
    
        zeiten = [datetime.strptime(zeit, "%H:%M") for zeit in zeiten] 
        return zeiten 

    else:
        print("Ungültige Eingabe. Bitte starte das Programm neu und gib '1' oder '2' ein.")
        exit()


def get_end_times(zeiten,lunch_time,target):
    # Differenz berechnen
    i=2
    # Lunch time berechnen
    pause = timedelta()
    for j in range(1, len(zeiten)-1, 2):
        pause += zeiten[j-1] - zeiten[j]

    if pause > lunch_time:
        lunch_time = pause

    end_time = zeiten[-1] + target + lunch_time
    return end_time


def get_transport_data(target_location, end_time, walking_time, minus_time):
    

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


def print_ascii (user,end_time):
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

def new_csv_entry():
    input("Benutzer nicht gefunden. Drücke Enter um einen neuen Eintrag zu erstellen...")
    user = input("Gib deinen Namen ein: ")
    username = input("Gib deinen Benutzernamen ein: ")
    target_location = input("Gib deinen Zielort ein (z.B. Rotkreuz, Hellbühl): ")
    walking_time = int(input("Gib deine Gehzeit zum Bahnhof in Minuten ein: "))
    minus_time = int(input("Wie viel früher möchtest du maximal gehen?: "))
    with open("preferences.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([user, username, target_location, walking_time, minus_time])
    

def main():
    # User-spezifische Einstellungen
    user = None
    try:
        user = os.getlogin()
    except Exception:
        user = None


    pref = pd.read_csv('ghc/preferences.csv')
    idx = pref.index[pref['username'] == user]
    if idx.empty:
        new_csv_entry()
        pref = pd.read_csv('ghc/preferences.csv')
        idx = pref.index[pref['username'] == user]

    target_location = pref.at[idx[0], 'target_location']
    walking_time = timedelta(minutes=int(pref.at[idx[0], 'walking_time']))
    minus_time = timedelta(minutes=int(pref.at[idx[0], 'minus_time']))
    target = timedelta(hours=8)
    lunch_time = timedelta(minutes=30)


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


    zeiten = get_times(decision)
    end_time = get_end_times(zeiten,lunch_time,target)

    print(f"Du musst bis \033[31m{end_time.strftime('%H:%M')}\033[0m arbeiten")



    get_transport_data(target_location, end_time, walking_time, minus_time)
    print_ascii(user, end_time)

if __name__ == "__main__":
    main()