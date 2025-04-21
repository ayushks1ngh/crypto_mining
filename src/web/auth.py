from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.id = username

class AuthManager:
    def __init__(self, config_path='config/users.json'):
        self.config_path = config_path
        self._ensure_config_exists()

    def _ensure_config_exists(self):
        if not os.path.exists(self.config_path):
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            self._save_users({'admin': generate_password_hash('admin')})

    def _load_users(self):
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_users(self, users):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(users, f)

    def validate_user(self, username, password):
        users = self._load_users()
        stored_hash = users.get(username)
        if stored_hash and check_password_hash(stored_hash, password):
            return User(username)
        return None

    def change_password(self, username, new_password):
        users = self._load_users()
        if username in users:
            users[username] = generate_password_hash(new_password)
            self._save_users(users)
            return True
        return False

auth_manager = AuthManager()