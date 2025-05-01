import requests
from rich import print

# API keys
webex_key = input("Geef je Webex API Key in aub: ")
webex_headers = {"Authorization": f"Bearer {webex_key}"}
cat_headers = {"x-api-key": "live_EZYC6zWcD75xxtCBwUbGZUTUsi3JCctk4us9NzaIyZTP3qNLUMpdzlsDRchTbiIu"}

# Basis urls
webex_url = "https://webexapis.com/v1/"
cat_url = "https://api.thecatapi.com/v1/"
prefix = "%"

# Hulpjes
def check_connection():
    webex_ok = requests.get(webex_url + "rooms", headers=webex_headers)
    cat_ok = requests.get(cat_url + "images", headers=cat_headers)
    if webex_ok.status_code == 200 and cat_ok.status_code == 200:
        print("[green]Connectie geslaagd[/green]")
    else:
        print("[red]Probleem met verbinding.[/red]")
        exit()