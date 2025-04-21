from flask import Flask, render_template, jsonify, request
from flask_login import LoginManager
from web.routes import web_bp
from web.auth import auth_manager, User
from mining.miner import MiningManager
from monitoring.system_monitor import SystemMonitor
from config.settings import load_config
import os

app = Flask(__name__, 
    template_folder=os.path.join(os.path.dirname(__file__), 'web/templates'))
    
# Load configuration
config = load_config()
app.config.update(config)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'web.login'

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Register blueprints
app.register_blueprint(web_bp)

# Initialize components
mining_manager = MiningManager()
system_monitor = SystemMonitor()

@app.route('/api/status')
def get_status():
    return jsonify({
        'system': system_monitor.get_stats(),
        'mining': mining_manager.get_status()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')