import requests
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

HUBSPOT_ACCESS_TOKEN = os.getenv('HUBSPOT_ACCESS_TOKEN')

def upload_to_hubspot(name, phone, cuit, email, business_type, attachment):
    url = "https://api.hubapi.com/crm/v3/objects/contacts"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "properties": {
            "firstname": name,
            "phone": phone,
            "cuit": cuit,
            "email": email,
            "business_type": business_type
        }
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def get_all_hubspot_clients():
    url = "https://api.hubapi.com/crm/v3/objects/contacts"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    params = {
        "limit": 100,
        "properties": ["firstname", "phone", "cuit", "email", "business_type"]
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    clients = response.json().get('results', [])
    return [
        {
            'id': client['id'],
            'name': client['properties'].get('firstname', ''),
            'phone': client['properties'].get('phone', ''),
            'cuit': client['properties'].get('cuit', ''),
            'email': client['properties'].get('email', ''),
            'business_type': client['properties'].get('business_type', '')
        } for client in clients
    ]
