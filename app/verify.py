import requests
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

HUBSPOT_ACCESS_TOKEN = os.getenv('HUBSPOT_ACCESS_TOKEN')

def verify_property(property_name):
    url = f"https://api.hubapi.com/crm/v3/properties/contacts/{property_name}"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(f"Property '{property_name}' exists in HubSpot.")
    else:
        print(f"Property '{property_name}' does NOT exist in HubSpot. Status Code: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    properties_to_check = ["firstname", "phone", "cuit", "email", "business_type"]
    for prop in properties_to_check:
        verify_property(prop)
