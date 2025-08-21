from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import users
from config import Config

bp = Blueprint('auth', __name__)

@bp.before_app_request
def ensure_admin_exists():
    # Crea admin si no existe
    if users.count_documents({"email": Config.ADMIN_EMAIL}) == 0:
        users.insert_one({
            "email": Config.ADMIN_EMAIL,
            "password": generate_password_hash(Config.ADMIN_PASSWORD),
            "role": "admin"
        })

@bp.get('/login')
def login_form():
    return render_template('login.html')

@bp.post('/login')
def login():
    email = request.form.get('email','').strip().lower()
    password = request.form.get('password','')
    u = users.find_one({"email": email})
    if not u or not check_password_hash(u['password'], password):
        flash('Credenciales inválidas', 'danger')
        return redirect(url_for('auth.login_form'))
    session['user_id'] = str(u['_id'])
    session['email'] = u['email']
    return redirect(url_for('index'))

@bp.get('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login_form'))
