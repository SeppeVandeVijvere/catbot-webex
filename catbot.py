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
def zoek_of_maak_room(naam):
    resp = requests.get(webex_url + "rooms", headers=webex_headers).json()
    for room in resp["items"]:
        if room["title"] == naam:
            print(f"[blue]Room gevonden: {naam}[/blue]")
            return room["id"]
    keuze = input(f"Room niet gevonden. Maken? (y/n): ")
    if keuze.lower() == "y":
        r = requests.post(webex_url + "rooms", headers=webex_headers, json={"title": naam}).json()
        print(f"[green]Room '{naam}' aangemaakt[/green]")
        return r["id"]
    exit()

def laatste_bericht(room_id):
    m = requests.get(webex_url + "messages", headers=webex_headers, params={"roomId": room_id, "max": 1}).json()
    return m["items"][0] if m["items"] else None

def stuur_kat(room_id, msg_id, soort="jpg", ras=None):
    zoek = {"mime_types": soort}
    if ras:
        zoek["breed_ids"] = ras
    resultaat = requests.get(cat_url + "images/search", headers=cat_headers, params=zoek).json()[0]
    url = resultaat["url"]
    extra = requests.get(cat_url + f"images/{resultaat['id']}", headers=cat_headers).json()
    tekst = "**Geen extra info.**"
    if extra.get("breeds"):
        b = extra["breeds"][0]
        tekst = f"**{b['name']}** uit {b['origin']}\n{b['temperament']}"
    body = {"roomId": room_id, "parentId": msg_id, "files": [url], "markdown": tekst}
    requests.post(webex_url + "messages", headers=webex_headers, json=body)