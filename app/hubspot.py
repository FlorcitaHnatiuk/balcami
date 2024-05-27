import requests
import os

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
            "hs_cuit": cuit,
            "email": email,
            "business_type": business_type
        }
    }

    print("Enviando datos a HubSpot:", data)

    response = requests.post(url, headers=headers, json=data)
    print("Respuesta de HubSpot:", response.status_code, response.text)
    response.raise_for_status()

def get_all_hubspot_clients():
    url = "https://api.hubapi.com/crm/v3/objects/contacts"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    params = {
        "limit": 100,
        "properties": ["firstname", "phone", "hs_cuit", "email", "business_type"]
    }

    response = requests.get(url, headers=headers, params=params)
    print("Respuesta de HubSpot (obtener clientes):", response.status_code, response.text)
    response.raise_for_status()

    clients = response.json().get('results', [])
    formatted_clients = []
    for client in clients:
        formatted_clients.append({
            'name': client['properties'].get('firstname', ''),
            'phone': client['properties'].get('phone', ''),
            'cuit': client['properties'].get('hs_cuit', ''),
            'email': client['properties'].get('email', ''),
            'business_type': client['properties'].get('business_type', '')
        })
    print("Clientes obtenidos de HubSpot:", formatted_clients)
    return formatted_clients
