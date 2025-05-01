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