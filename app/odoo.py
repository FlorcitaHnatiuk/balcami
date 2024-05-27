import requests
import os

ODOO_URL = os.getenv('ODOO_URL')
ODOO_DB = os.getenv('ODOO_DB')
ODOO_USERNAME = os.getenv('ODOO_USERNAME')
ODOO_PASSWORD = os.getenv('ODOO_PASSWORD')
ODOO_API_KEY = os.getenv('ODOO_API_KEY')

def authenticate_odoo():
    try:
        response = requests.post(f'{ODOO_URL}/web/session/authenticate', json={
            'jsonrpc': '2.0',
            'method': 'call',
            'params': {
                'db': ODOO_DB,
                'login': ODOO_USERNAME,
                'password': ODOO_PASSWORD,
            },
            'id': int(os.urandom(1)[0])
        })
        response_data = response.json()
        print("Respuesta de autenticación:", response_data)
        response.raise_for_status()
        result = response_data.get('result')
        if not result:
            print('Error de autenticación en Odoo:', response_data)
            return None

        session_id = response.cookies.get('session_id')
        print(f'Autenticación exitosa con Odoo. session_id: {session_id}')
        return session_id
    except requests.exceptions.RequestException as e:
        print('Error autenticando con Odoo:', e)
        raise

def upload_to_odoo(name, phone, cuit, email, business_type, attachment):
    session_id = authenticate_odoo()
    if not session_id:
        print('No se pudo autenticar con Odoo. Datos no enviados.')
        return

    headers = {
        'Cookie': f'session_id={session_id}',
        'Authorization': f'Bearer {ODOO_API_KEY}'
    }
    data = {
        'name': name,
        'phone': phone,
        'x_cuit': cuit,
        'email': email,
        'x_business_type': business_type
    }

    print("Enviando datos a Odoo:", data)

    try:
        response = requests.post(f'{ODOO_URL}/web/dataset/call_kw', headers=headers, json={
            'jsonrpc': '2.0',
            'method': 'call',
            'params': {
                'model': 'res.partner',
                'method': 'create',
                'args': [data],
                'kwargs': {},
            },
            'id': int(os.urandom(1)[0])
        })
        print("Respuesta de Odoo:", response.status_code, response.text)
        response.raise_for_status()
        if response.json().get('result'):
            print('Cliente subido a Odoo exitosamente.')
        else:
            print('Error al subir a Odoo:', response.text)
    except requests.exceptions.RequestException as e:
        print('Error al subir a Odoo:', e)
        raise

def get_all_odoo_clients():
    session_id = authenticate_odoo()
    if not session_id:
        print('No se pudo autenticar con Odoo. No se pueden obtener clientes.')
        return []

    headers = {
        'Cookie': f'session_id={session_id}',
        'Authorization': f'Bearer {ODOO_API_KEY}'
    }

    try:
        response = requests.post(f'{ODOO_URL}/web/dataset/call_kw', headers=headers, json={
            'jsonrpc': '2.0',
            'method': 'call',
            'params': {
                'model': 'res.partner',
                'method': 'search_read',
                'args': [[]],  # Filtrar todos los registros
                'kwargs': {
                    'fields': ['name', 'phone', 'x_cuit', 'email', 'x_business_type'],  # Asegúrate de que 'x_cuit' y 'x_business_type' existen
                },
            },
            'id': int(os.urandom(1)[0])
        })
        print("Respuesta de Odoo (obtener clientes):", response.status_code, response.text)
        response.raise_for_status()
        clients = response.json().get('result', [])
        formatted_clients = []
        for client in clients:
            formatted_clients.append({
                'name': client.get('name', ''),
                'phone': client.get('phone', ''),
                'cuit': client.get('x_cuit', ''),
                'email': client.get('email', ''),
                'business_type': client.get('x_business_type', '')
            })
        print("Clientes obtenidos de Odoo:", formatted_clients)
        return formatted_clients
    except requests.exceptions.RequestException as e:
        print('Error al obtener clientes de Odoo:', e)
        raise
