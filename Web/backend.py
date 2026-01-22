from fastapi import FastAPI
from ghc.get_menus import get_menus
from datetime import datetime, timedelta
from pydantic import BaseModel


class Item(BaseModel):
    string: list[datetime]
    lunch_time: timedelta | None = None
    target: timedelta | None = None
# Example
#    {
#  "string": ["2026-01-22T12:14:00+01:00","2026-01-22T11:31:00+01:00","2026-01-22T07:41:00+01:00"],
#  "lunch_time": "P0Y0M0DT0H30M0S",
#  "target": "P0Y0M0DT8H0M0S"
#    }

app = FastAPI()

@app.post("/calc")
def get_end_times(item: Item):
    # Differenz berechnen
    times = item.string 
    target = item.target or timedelta(hours=8)
    lunch_time = item.lunch_time or timedelta(minutes=30)
    # Lunch time berechnen
    pause = timedelta()
    for j in range(1, len(times)-1, 2):
        pause += times[j-1] - times[j]

    if pause > lunch_time:
        lunch_time = pause
    print(f"Pause: {lunch_time}, Zielzeit: {target}, Zeiten: {times[-1]}")
    end_time = times[-1] + target + lunch_time
    return end_time

@app.get("/menus")
async def menus():
        menu_json = {}
        menus = get_menus()
        for name, desc, sort in menus:
            menu_json[sort]= {"name": name, "desc": desc}
        return menu_json


'''
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
        
        if verbindung["from"].get("delay") is not None and verbindung["from"].get("delay") > 3:
            print(f"  {abfahrt.strftime('%H:%M')} Uhr (Verspätung: {verbindung['from']['delay']} Min.)")
        else:
            print(f"  {abfahrt.strftime('%H:%M')} Uhr")



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
    with open("ghc/preferences.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([user, username, target_location, walking_time, minus_time])
    
def set_data():
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
    return user, target_location, walking_time, minus_time, target, lunch_time

def main():
    # User-spezifische Einstellungen

    user, target_location, walking_time, minus_time, target, lunch_time = set_data()

    # Auswahl: Text oder OCR
    print("Text oder OCR")
    decision = input("Gib '1' für Text, '2' für OCR, '3' für Menüs ein: ")
    print()

    if decision == '1' or decision == '2':
        zeiten = get_times(decision)
        end_time = get_end_times(zeiten,lunch_time,target)

        print(f"Du musst bis \033[31m{end_time.strftime('%H:%M')}\033[0m arbeiten")
        working_to = end_time - datetime.now()
        working_datetime = datetime(2000, 1, 1) + working_to
        print(f"Du musst noch \033[31m{working_datetime.strftime('%H:%M')}\033[0m arbeiten bis Feierabend!")



        get_transport_data(target_location, end_time, walking_time, minus_time)
        print_ascii(user, end_time)

    elif decision == '3':
        print("Heutige Menüs im Personalrestaurant:")
        print()
        menus = get_menus()
        for name, desc, sort in menus:
            print("Menü Name:", name)
            print("Beschreibung:", desc)
            print("Type:", sort)
            print("-" * 40)
    
try:
    if __name__ == "__main__":
        main()
except Exception as e:
    print("Ein Fehler ist aufgetreten:", str(e))
    input("Drücke Enter um das Programm zu beenden...")'''