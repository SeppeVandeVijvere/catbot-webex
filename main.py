from webex_api import *
from cat_api import *
from rich import print

# API keys
webex_key = input("Geef je Webex API Key in: ")
webex_headers = {"Authorization": f"Bearer {webex_key}"}
cat_headers = {"x-api-key": "live_EZYC6zWcD75xxtCBwUbGZUTUsi3JCctk4us9NzaIyZTP3qNLUMpdzlsDRchTbiIu"}

check_connection(webex_headers)
room_id = zoek_of_maak_room(input("Room naam: "), webex_headers)
laatste_id = ""

print("[cyan]Starten met luisteren...[/cyan]")
while True:
    m = laatste_bericht(room_id, webex_headers)
    if m and m["id"] != laatste_id and m["text"].startswith("%"):
        parts = m["text"].split(" ", 1)
        cmd = parts[0][1:]
        arg = parts[1] if len(parts) > 1 else None
        if cmd == "cat":
            id = haal_breed_id(arg, cat_headers) if arg else None
            stuur_kat(room_id, m["id"], webex_headers, cat_headers, "jpg", id)
        elif cmd == "gif":
            id = haal_breed_id(arg, cat_headers) if arg else None
            stuur_kat(room_id, m["id"], webex_headers, cat_headers, "gif", id)
        elif cmd == "breeds" or cmd == "rassen":
            stuur_rassen(room_id, m["id"], webex_headers, cat_headers)
        elif cmd == "info" and arg:
            stuur_info(room_id, m["id"], arg, webex_headers, cat_headers)
        laatste_id = m["id"]