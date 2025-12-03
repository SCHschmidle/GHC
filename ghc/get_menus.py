import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://clients.eurest.ch/schindler/de/Internes%20Personalrestaurant'  

def get_menus():
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        menus = soup.find_all("div", class_="list-item")
        menu_list = []
        for menu in menus:
            name = menu.find("h3").get_text(strip=True)
            desc = menu.find("p").get_text(strip=True)
            sort = menu.find("span").get_text(strip=True)
            menu_list.append((name, desc, sort))
        return menu_list
    else:
        print(f"Fehler beim Abrufen der Seite: {response.status_code}")
        return []