from flask import Flask, request, render_template, jsonify
from odoo import upload_to_odoo, get_all_odoo_clients
from hubspot import upload_to_hubspot, get_all_hubspot_clients

app = Flask(__name__)
app.secret_key = '1234'  # Cambia esto por una clave secreta segura

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    phone = request.form['phone']
    cuit = request.form['cuit']
    email = request.form['email']
    business_type = request.form['business_type']
    crms = request.form.getlist('crms')
    attachment = request.files.get('attachment')

    success_crms = []
    errors = []

    if 'odoo' in crms:
        try:
            upload_to_odoo(name, phone, cuit, email, business_type, attachment)
            success_crms.append('Odoo')
        except Exception as e:
            errors.append(f'Error al subir a Odoo: {e}')

    if 'hubspot' in crms:
        try:
            upload_to_hubspot(name, phone, cuit, email, business_type, attachment)
            success_crms.append('HubSpot')
        except Exception as e:
            errors.append(f'Error al subir a HubSpot: {e}')

    if errors:
        return jsonify({'status': 'error', 'message': 'Hubo un problema al crear el cliente', 'errors': errors})

    return jsonify({'status': 'success', 'message': 'Cliente creado correctamente', 'crms': success_crms})

@app.route('/unified-info')
def unified_info():
    odoo_clients = get_all_odoo_clients()
    hubspot_clients = get_all_hubspot_clients()

    for client in odoo_clients:
        client['source'] = 'Odoo'
    for client in hubspot_clients:
        client['source'] = 'HubSpot'

    all_clients = odoo_clients + hubspot_clients
    return render_template('unified_info.html', clients=all_clients)

if __name__ == '__main__':
    app.run(debug=True)
