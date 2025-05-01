# Webex CatBot

## Overzicht
Deze Python-bot communiceert via de Webex API en TheCatAPI. De bot luistert naar commando's in een Webex-room en reageert met kattenafbeeldingen, gifs, of informatie over kattenrassen.

## Vereisten
- Python 3.x
- Internetverbinding
- Geldige Webex API-key
- Geldige Cat API-key (hardcoded)

## Gebruik
Bij het starten vraagt het script om:
- Een Webex API-key
- Een roomnaam

Indien de room niet bestaat, wordt de gebruiker gevraagd of deze aangemaakt moet worden.

## Commando's
Gebruik commando's in de Webex-room voorafgegaan door `%`:

- `%cat [ras]`  
  Stuurt een JPG-afbeelding van een kat. Indien ras gespecificeerd, toont enkel dat ras.

- `%gif [ras]`  
  Stuurt een GIF van een kat. Optioneel kan een ras meegegeven worden.

- `%breeds`  
  Toont een lijst van beschikbare kattenrassen.

- `%rassen`  
  Alternatieve naam voor `%breeds`.

- `%info [ras]`  
  Geeft beschrijving, herkomst en temperament van een specifiek ras.

## Bestanden
- `main.py` (hoofdscript met alle functionaliteit)
- `README.md` (deze uitleg)

## APIs
- [Webex API](https://developer.webex.com/docs/api/v1/)
- [TheCatAPI](https://thecatapi.com/)

## Belangrijke headers
- Webex: `"Authorization": "Bearer <webex_key>"`
- Cat API: `"x-api-key": "<hardcoded_key>"`

## Output
- Reacties in Webex met tekst en/of afbeeldingen
- Terminaloutput met verbindingsstatus en foutmeldingen