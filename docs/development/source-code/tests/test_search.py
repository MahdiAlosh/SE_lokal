# test_search.py

# tests/test_search.py

import sys
import os

# Füge das Verzeichnis zum PYTHONPATH hinzu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pytest
from flask_testing import TestCase
from flask_login import login_user, current_user
from website import create_app, db
from website.models import User
from werkzeug.security import generate_password_hash

class TestSearch(TestCase):

    def create_app(self):
        # Konfigurieren der Flask-Anwendung für Tests
        test_config = {
            'TESTING': True,
            'WTF_CSRF_ENABLED': False,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
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
        # Einloggen des Testbenutzers
        with self.client:
            login_user(user)

    def tearDown(self):
        # Datenbank am Ende des Tests leeren
        db.session.remove()
        db.drop_all()

    def test_search_page_loaded(self):
        # Testen, ob die Suchseite geladen wird und der Benutzer authentifiziert ist
        response = self.client.get('/search')
        self.assert200(response)
        self.assertTrue(current_user.is_authenticated)

    def test_search_with_invalid_input(self):
        # Testen der Suche mit ungültiger Eingabe
        response = self.client.post('/search', data=dict(
            eingabe=''
        ), follow_redirects=True)

        self.assert200(response)
        # Überprüfen, ob die Fehlermeldung korrekt angezeigt wird
        self.assertIn('Please enter a valid company name.', response.data.decode())

    def test_successful_search(self):
        # Testen einer erfolgreichen Suche
        response = self.client.post('/search', data=dict(
            eingabe='Telekom'
        ), follow_redirects=True)
        
        self.assert200(response)
        # Überprüfen, ob die erwartete Antwort in der Antwort enthalten ist

    def test_search_with_no_result(self):
        # Testen der Suche, wenn keine Ergebnisse gefunden werden
        # Möglicherweise eine Mocking-Bibliothek verwenden, um die Wikipedia-Antwort zu simulieren
        pass  # TODO

if __name__ == '__main__':
    pytest.main()
