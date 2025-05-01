import requests
from rich import print

webex_url = "https://webexapis.com/v1/"

def check_connection(webex_headers):
    try:
        webex_ok = requests.get(webex_url + "rooms", headers=webex_headers)
        print(f"Webex status code: {webex_ok.status_code}")
        if webex_ok.status_code != 200:
            raise Exception(f"Webex API fout: {webex_ok.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[red]Verbindingsfout: {str(e)}[/red]")
        exit()

def zoek_of_maak_room(naam, webex_headers):
    try:
        resp = requests.get(webex_url + "rooms", headers=webex_headers).json()
        for room in resp.get("items", []):
            if room["title"] == naam:
                print(f"[blue]Room gevonden: {naam}[/blue]")
                return room["id"]

        keuze = input(f"Room niet gevonden. Maken? (y/n): ")
        if keuze.lower() == "y":
            r = requests.post(webex_url + "rooms", headers=webex_headers, json={"title": naam}).json()
            if "id" not in r:
                raise Exception("Fout bij het aanmaken van de room.")
            print(f"[green]Room '{naam}' aangemaakt[/green]")
            return r["id"]
        exit()
    except requests.exceptions.RequestException as e:
        print(f"[red]Webex request fout: {str(e)}[/red]")
        exit()
    except Exception as e:
        print(f"[red]Fout: {str(e)}[/red]")
        exit()

def laatste_bericht(room_id, webex_headers):
    m = requests.get(webex_url + "messages", headers=webex_headers, params={"roomId": room_id, "max": 1}).json()
    return m["items"][0] if m["items"] else None

def stuur_bericht(room_id, msg_id, markdown, webex_headers):
    body = {
        "roomId": room_id,
        "parentId": msg_id,
        "markdown": markdown
    }
    requests.post(webex_url + "messages", headers=webex_headers, json=body)