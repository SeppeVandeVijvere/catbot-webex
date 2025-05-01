import requests
from rich import print as rprint
import time

# ———————————————————————————————————————— 
# CONFIGURATIE 
# ———————————————————————————————————————— 

# 1) Webex-API key (voer in bij prompt)
api_sleutel_input = input("Voer je Webex API-sleutel in: ").strip()
webex_api_sleutel = "Bearer " + api_sleutel_input

# 2) Basis-parameters Webex
webex_basis_url = "https://webexapis.com/v1/"
webex_headers = {"Authorization": webex_api_sleutel}

# 3) Commando-prefix
prefix = "!"

# 4) Cat API key (demo-sleutel)
kat_api_sleutel = "live_EZYC6zWcD75xxtCBwUbGZUTUsi3JCctk4us9NzaIyZTP3qNLUMpdzlsDRchTbiIu"
kat_basis_url = "https://api.thecatapi.com/v1/"
kat_headers = {"x-api-key": kat_api_sleutel}

# ———————————————————————————————————————— 
# FUNCTIES VOOR ROOM MANAGEMENT 
# ———————————————————————————————————————— 

def zoek_kamer(kamer_naam):
    resp = requests.get(webex_basis_url + "rooms", headers=webex_headers).json()
    for kamer in resp.get("items", []):
        if kamer.get("title") == kamer_naam:
            rprint(f"[green]Kamer gevonden:[/green] {kamer_naam} (ID: {kamer['id']})")
            return kamer["id"]
    return None

def maak_kamer(kamer_naam):
    body = {"title": kamer_naam}
    resp = requests.post(webex_basis_url + "rooms", headers=webex_headers, json=body).json()
    kamer_id = resp.get("id")
    rprint(f"[green]Kamer aangemaakt:[/green] {kamer_naam} (ID: {kamer_id})")
    return kamer_id

def krijg_of_maak_kamer(naam):
    kamer_id = zoek_kamer(naam)
    if kamer_id:
        return kamer_id
    antwoord = input(f"Kamer '{naam}' niet gevonden. Aanmaken? (j/n): ")
    if antwoord.lower().startswith("j"):
        return maak_kamer(naam)
    rprint("[red]Geen kamer gekozen — programma wordt afgesloten[/red]")
    exit()

# ———————————————————————————————————————— 
# CAT API FUNCTIES 
# ———————————————————————————————————————— 

def haal_rassenlijst_op():
    return requests.get(kat_basis_url + "breeds", headers=kat_headers).json()

def zoek_ras_id(naam):
    for ras in haal_rassenlijst_op():
        if ras["name"].lower() == naam.lower():
            return ras["id"]
    return None

def haal_katafbeelding(mime="jpg", ras_id=None):
    params = {"mime_types": mime}
    if ras_id:
        params["breed_ids"] = ras_id
    afbeeldingen = requests.get(kat_basis_url + "images/search", headers=kat_headers, params=params).json()
    return afbeeldingen[0] if afbeeldingen else None

def haal_info_over_afbeelding(afbeelding_id):
    data = requests.get(kat_basis_url + f"images/{afbeelding_id}", headers=kat_headers).json()
    if data.get("breeds"):
        b = data["breeds"][0]
        tekst = f"**{b['name']}** uit {b['origin']}\nTemperament: {b['temperament']}\nLevensduur: {b['life_span']} jaar"
        if b.get("wikipedia_url"):
            tekst += f"\n[Meer info]({b['wikipedia_url']})"
        return tekst
    return "**Geen extra info**"

# ———————————————————————————————————————— 
# WEBEX BERICHTFUNCTIES 
# ———————————————————————————————————————— 

def stuur_bericht(kamer_id, ouder_id, markdown=None, bestanden=None):
    body = {"roomId": kamer_id}
    if ouder_id:
        body["parentId"] = ouder_id
    if markdown:
        body["markdown"] = markdown
    if bestanden:
        body["files"] = bestanden
    requests.post(webex_basis_url + "messages", headers=webex_headers, json=body)

def stuur_kat(kamer_id, bericht_id, mime, ras_id=None):
    afbeelding = haal_katafbeelding(mime, ras_id)
    if not afbeelding:
        stuur_bericht(kamer_id, bericht_id, markdown="❌ Kan geen afbeelding ophalen.")
        return
    info = haal_info_over_afbeelding(afbeelding["id"])
    stuur_bericht(kamer_id, bericht_id, markdown=info, bestanden=[afbeelding["url"]])

def stuur_rassen(kamer_id, bericht_id):
    lijst = "\n".join(f"- {r['name']}" for r in haal_rassenlijst_op())
    stuur_bericht(kamer_id, bericht_id, markdown="**Beschikbare rassen:**\n" + lijst)

def stuur_info(kamer_id, bericht_id, ras_naam):
    ras_id = zoek_ras_id(ras_naam)
    if not ras_id:
        stuur_bericht(kamer_id, bericht_id, markdown=f"❌ Ras '{ras_naam}' niet gevonden.")
    else:
        afbeelding = haal_katafbeelding("jpg", ras_id)
        info = haal_info_over_afbeelding(afbeelding["id"])
        stuur_bericht(kamer_id, bericht_id, markdown=info, bestanden=[afbeelding["url"]])

# ———————————————————————————————————————— 
# FUNCTIE OM LAATSTE BERICHT TE HALEN 
# ———————————————————————————————————————— 

def laatste_bericht(kamer_id):
    resp = requests.get(
        webex_basis_url + f"messages?roomId={kamer_id}&max=1",
        headers=webex_headers
    ).json()
    berichten = resp.get("items", [])
    return berichten[0] if berichten else None

# ———————————————————————————————————————— 
# CONNECTIVITEITSCHECK 
# ———————————————————————————————————————— 

def controleer_verbinding():
    try:
        w = requests.get(webex_basis_url + "rooms", headers=webex_headers, timeout=5)
        c = requests.get(kat_basis_url + "images", headers=kat_headers, timeout=5)
        if w.status_code == 200 and c.status_code == 200:
            rprint("[green]API’s bereikbaar[/green]")
        else:
            rprint(f"[red]API-fout: Webex {w.status_code}, Kat {c.status_code}[/red]")
            exit()
    except Exception as fout:
        rprint(f"[red]Verbindingsfout: {fout}[/red]")
        exit()

# ———————————————————————————————————————— 
# HOOFDSCRIPT 
# ———————————————————————————————————————— 

controleer_verbinding()
kamer_naam = input("Kamernaam: ")
kamer_id = krijg_of_maak_kamer(kamer_naam)

rprint(f"[cyan]Luister naar berichten in '{kamer_naam}' (prefix '{prefix}')[/cyan]")

laatste_id = None
while True:
    bericht = laatste_bericht(kamer_id)

    if bericht and bericht["id"] != laatste_id and bericht.get("text", "").startswith(prefix):
        delen = bericht["text"].split(" ", 1)
        commando = delen[0][1:].lower()
        argument = delen[1] if len(delen) > 1 else None

        if commando == "cat":
            ras_id = zoek_ras_id(argument) if argument else None
            stuur_kat(kamer_id, bericht["id"], "jpg", ras_id)
        elif commando == "gif":
            ras_id = zoek_ras_id(argument) if argument else None
            stuur_kat(kamer_id, bericht["id"], "gif", ras_id)
        elif commando in ("rassen", "breeds"):
            stuur_rassen(kamer_id, bericht["id"])
        elif commando == "info" and argument:
            stuur_info(kamer_id, bericht["id"], argument)

        laatste_id = bericht["id"]

    time.sleep(1)

# TESTCOMMANDO'S VOOR FILMPJE
stuur_rassen("dummy_kamer_id", None)
stuur_kat("dummy_kamer_id", None, "jpg")
stuur_info("dummy_kamer_id", None, "Abyssinian")