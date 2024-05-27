# Balcami Test Técnico

## Descripción

Este proyecto es una aplicación web desarrollada con Flask que permite a los vendedores de Balcami subir información de clientes a los CRMs HubSpot y Odoo desde un solo formulario. Además, unifica la información de ambos CRMs en una sola página.

## Requisitos

- Python 3.6+
- Flask
- requests
- python-dotenv
- xmlrpc.client (este viene incluido con Python)

## Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/FlorcitaHnatiuk/balcami.git
   cd balcami
   cd app

2. **Crear y activar un entorno virtual**

    ```python3 -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`

3. **Instalar las dependencias:**

    ```pip install flask requests python-dotenv

4. **Configurar las variables de entorno:**
Crea un archivo .env en la raíz del proyecto con las siguientes variables (modifica con tus credenciales reales):

ODOO_API=tu_odoo_api
ODOO_URL=https://tu_odoo_instance_url
ODOO_DB=tu_odoo_db
ODOO_USERNAME=tu_odoo_username
ODOO_PASSWORD=tu_odoo_password
HUBSPOT_API_KEY=tu_hubspot_api_key
HUBSPOT_SECRET=tu_hubspot_secret

5. **Ejecutá la app**

    ```python3 app.py

6. **Acceder a la app:**

Abre tu navegador web y navega a http://localhost:5000 para ver el formulario de subida de datos.
Navega a http://localhost:5000/unified-info para ver la información unificada de los clientes.

