from flask import Flask, request, render_template, jsonify, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import os
from odoo import upload_to_odoo, get_all_odoo_clients
from hubspot import upload_to_hubspot, get_all_hubspot_clients

app = Flask(__name__)
app.secret_key = '1234'  # Cambia esto por una clave secreta segura

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simulación de base de datos de usuarios
users = {'admin': {'password': 'admin123'}}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    if username not in users:
        return None
    return User(username)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            flash('Login successful.')
            return redirect(url_for('unified_info'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

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
    try:
        if 'odoo' in crms:
            upload_to_odoo(name, phone, cuit, email, business_type, attachment)
            success_crms.append('Odoo')
        if 'hubspot' in crms:
            upload_to_hubspot(name, phone, cuit, email, business_type, attachment)
            success_crms.append('HubSpot')

        return jsonify({'status': 'success', 'message': 'Cliente creado correctamente', 'crms': success_crms})
    except Exception as e:
        print(f'Error al crear el cliente: {e}')
        return jsonify({'status': 'error', 'message': 'Hubo un problema al crear el cliente'})

@app.route('/unified-info')
@login_required
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
