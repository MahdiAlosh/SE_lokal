# tests/test_auth.py

import sys
import os

# Füge das Verzeichnis zum PYTHONPATH hinzu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pytest
from flask_testing import TestCase
from flask_login import current_user
from website import create_app, db
from website.models import User
from werkzeug.security import generate_password_hash

class TestAuth(TestCase):

    def create_app(self):
        # Konfigurieren der Flask-Anwendung für Tests
        test_config = {
            'TESTING': True,
            'WTF_CSRF_ENABLED': False,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False  # Optional: um unnötige Warnungen zu vermeiden und Ressourcen zu sparen
        }
        # Erstellen einer Anwendung mit Testkonfiguration
        app = create_app(test_config)
        return app

    def setUp(self):
        # Datenbank initialisieren und Testbenutzer erstellen
        db.create_all()
        user = User(email='test@example.com', password=generate_password_hash('test', method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()


    def tearDown(self):
        # Datenbank am Ende des Tests leeren
        db.session.remove()
        db.drop_all()

    def test_login_page(self):
        # Testen, ob die Login-Seite geladen wird
        response = self.client.get('/login')
        self.assert200(response)

    def test_successful_login(self):
        # Testen eines erfolgreichen Logins
        response = self.client.post('/login', data=dict(
            email='test@example.com',
            password='test'
        ), follow_redirects=True)
        
        self.assert200(response)
        self.assertTrue(current_user.is_authenticated)

    def test_failed_login(self):
        # Testen eines fehlgeschlagenen Logins
        response = self.client.post('/login', data=dict(
            email='test@example.com',
            password='wrongpassword'
        ), follow_redirects=True)
        
        self.assert200(response)
        self.assertFalse(current_user.is_authenticated)

if __name__ == '__main__':
    pytest.main()
