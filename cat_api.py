import requests
from rich import print

cat_url = "https://api.thecatapi.com/v1/"

def stuur_kat(room_id, msg_id, webex_headers, cat_headers, soort="jpg", ras=None):
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
    
    from webex_api import stuur_bericht
    stuur_bericht(room_id, msg_id, f"![Cat]({url})\n\n{tekst}", webex_headers)

def haal_breed_id(naam, cat_headers):
    lijst = requests.get(cat_url + "breeds", headers=cat_headers).json()
    for b in lijst:
        if naam.lower() == b["name"].lower():
            return b["id"]
    return None

def stuur_rassen(room_id, msg_id, webex_headers, cat_headers):
    lijst = requests.get(cat_url + "breeds", headers=cat_headers).json()
    namen = "\n".join(f"- {b['name']}" for b in lijst)
    from webex_api import stuur_bericht
    stuur_bericht(room_id, msg_id, f"**Beschikbare rassen:**\n{namen}", webex_headers)

def stuur_info(room_id, msg_id, ras_naam, webex_headers, cat_headers):
    lijst = requests.get(cat_url + "breeds", headers=cat_headers).json()
    ras = next((b for b in lijst if ras_naam.lower() == b["name"].lower()), None)
    if not ras:
        markdown = f"❌ Ras '{ras_naam}' niet gevonden."
    else:
        markdown = f"**{ras['name']}**\nHerkomst: {ras['origin']}\nTemperament: {ras['temperament']}\nBeschrijving: {ras['description']}"
    
    from webex_api import stuur_bericht
    stuur_bericht(room_id, msg_id, markdown, webex_headers)