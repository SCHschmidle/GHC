import warnings
warnings.filterwarnings("ignore")
from datetime import timedelta
import urllib3
import os
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
zeiten = get_times('2')
end_time = get_end_times(zeiten,lunch_time,target)
print(f"Du musst bis \033[31m{end_time.strftime('%H:%M')}\033[0m arbeiten")
get_transport_data(target_location, end_time, walking_time, minus_time)
print_ascii(user, end_time)
