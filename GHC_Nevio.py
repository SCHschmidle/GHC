import re
from datetime import datetime, timedelta
import requests
from datetime import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# sTylyling
print(r"""                                                               
  _______   ______      __    __    ______    ___  ___   _______      ______     ___       __        ______ 
 /  _____| /  __  \    |  |  |  |  /  __  \  |   \/   | |   ____|    /      |   /   \     |  |      /      |
|  |  __  |  |  |  |   |  |__|  | |  |  |  | |  \  /  | |  |__      |  ,----'  /  ^  \    |  |     |  ,----'
|  | |_ | |  |  |  |   |   __   | |  |  |  | |  |\/|  | |   __|     |  |      /  /_\  \   |  |     |  |     
|  |__| | |  `--'  |   |  |  |  | |  `--'  | |  |  |  | |  |____    |  `----./  _____  \  |  `----.|  `----.
 \______|  \______/ [_]|__|  |__|  \______/  |__|  |__| |_______|[_] \______/__/     \__\ |_______| \______|
                                                                                                             
 -   ____________ ____________ ____________ 7 ____________ ____________ 7 ____________ ____________ ____________
--  / #  #  #  # ¦ #  #  #  # ¦ #  #  #  # ¦¨¦ #  #  #  # ¦ #  #  #  # ¦¨¦ #  #  #  # ¦ #  #  #  # ¦ #  #  #  # \\
 -- °°¨¨¨¨¨¨¨¨¨¨¨°¨¨¨¨¨¨¨¨¨¨¨¨°¨¨¨¨¨¨¨¨¨¨¨¨°°°¨¨¨¨¨¨¨¨¨¨¨¨°¨¨¨¨¨¨¨¨¨¨¨¨°°°¨¨¨¨¨¨¨¨¨¨¨¨°¨¨¨¨¨¨¨¨¨¨¨¨°¨¨¨¨¨¨¨¨¨¨¨°°
""")


print("------------------------------------------------------------------------------------------------------------------ \n \n")

text = input("Gib mir deine TimeTool Zeiten: ")
print()

# Regex ohne \b, nur nach Muster HH:MM suchen
zeiten = re.findall(r'\d{1,2}:\d{2}', text)

#print(zeiten)
# Zwei Zeiten als strings
zeit1 = zeiten[0]
zeit2 = zeiten[1]
zeit3 = zeiten[2]

# In datetime-Objekte konvertieren
t1 = datetime.strptime(zeit1, "%H:%M") # Start after lunch
t2 = datetime.strptime(zeit2, "%H:%M") # End before lunch
t3 = datetime.strptime(zeit3, "%H:%M") # Start morning
target = timedelta(hours=8)

# Differenz berechnen
differenz = t2 - t3
print(f"Du hast {differenz} gearbeitet")

if (t1-t2<timedelta(minutes=30)):
    t1 = t2+timedelta(minutes=30)
end_time = t1 + target - differenz
print(f"Du musst bis {end_time.strftime('%H:%M')} arbeiten")

r = requests.get(f"https://transport.opendata.ch/v1/connections?from=Buchrain&to=Rotkreuz&time={(end_time + timedelta(minutes=7)).strftime('%H:%M')}&limit=4", verify=False)
data = r.json()
print()
print("Nächste Abfahrten ab Buchrain:")
for verbindung in data["connections"]:
    abfahrt = datetime.fromisoformat(verbindung["from"]["departure"])
    print(f"  {abfahrt.strftime('%H:%M')} Uhr")