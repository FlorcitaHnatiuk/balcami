from flask import Flask, request, render_template, redirect, url_for, jsonify
import os
from odoo import upload_to_odoo, get_all_odoo_clients
from hubspot import upload_to_hubspot, get_all_hubspot_clients


app = Flask(__name__)

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
    crms = request.form.getlist('crms')  # Lista de CRMs seleccionados
    attachment = request.files.get('attachment')

    # Subir a Odoo si está seleccionado
    if 'odoo' in crms:
        upload_to_odoo(name, phone, cuit, email, business_type, attachment)

    # Subir a HubSpot si está seleccionado
    if 'hubspot' in crms:
        upload_to_hubspot(name, phone, cuit, email, business_type, attachment)

    return redirect(url_for('index'))

@app.route('/unified-info')
def unified_info():
    # Obtener clientes de ambos CRMs
    odoo_clients = get_all_odoo_clients()
    hubspot_clients = get_all_hubspot_clients()

    # Unificar la información
    all_clients = odoo_clients + hubspot_clients

    return render_template('unified_info.html', clients=all_clients)

if __name__ == '__main__':
    app.run(debug=True)
