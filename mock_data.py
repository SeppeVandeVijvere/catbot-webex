# mock_data.py

# Mock Webex API
def mock_get_rooms():
    # Dit simuleert het ophalen van kamers van de Webex API
    return {
        "items": [
            {"id": "room123", "title": "TestRoom"}
        ]
    }

def mock_send_message(room_id, parent_id=None, markdown=None, files=None):
    # Dit simuleert het versturen van een bericht naar een Webex-kamer
    print(f"Bericht verzonden naar kamer {room_id}. Markdown: {markdown}, Bestanden: {files}")

# Mock Cat API
def mock_get_breeds():
    # Dit simuleert het ophalen van kattenrassen van de Cat API
    return [
        {"id": "persian", "name": "Persian"},
        {"id": "bengal", "name": "Bengal"}
    ]

def mock_get_cat_image(mime="jpg", breed_id=None):
    # Dit simuleert het ophalen van een kattenafbeelding
    return {"id": "cat123", "url": "https://example.com/cat_image.jpg"}

def mock_get_rooms():
    return {
        "items": [
            {"id": "room1", "title": "Room 1"},
            {"id": "room2", "title": "Room 2"},
            {"id": "room3", "title": "Room 3"}
        ]
    }