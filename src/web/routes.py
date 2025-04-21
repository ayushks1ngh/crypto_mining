from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from .auth import auth_manager

web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('web.dashboard'))
    return render_template('index.html')

@web_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = auth_manager.validate_user(username, password)
        if user:
            login_user(user)
            return redirect(url_for('web.dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@web_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('web.index'))

@web_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@web_bp.route('/api/start', methods=['POST'])
@login_required
def start_mining():
    config = request.get_json()
    from app import mining_manager
    return jsonify(mining_manager.start_mining(config))

@web_bp.route('/api/stop', methods=['POST'])
@login_required
def stop_mining():
    from app import mining_manager
    return jsonify(mining_manager.stop_mining())