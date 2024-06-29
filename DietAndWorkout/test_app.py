import unittest
from app import app, db
from models import User
from flask import url_for
from werkzeug.security import generate_password_hash

class BasicTests(unittest.TestCase):

    # Zainicjalizowanie środowiska testowego
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    # Czyszczenie środowiska testowego
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Testowanie glownej strony
    def test_home_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)

    # Testowanie rejestracji uzytkownika
    def test_register(self):
        response = self.app.post('/register', data=dict(
            username='newuser',
            email='newuser@example.com',
            password='newpassword123',
            confirm='newpassword123'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Rejestracja', response.data)

    # Testowanie logowania uzytkownika
    def test_login(self):
        hashed_password = generate_password_hash('newpassword123', method='pbkdf2:sha256')
        with app.app_context():
            user = User(username='newuser', email='newuser@example.com', password=hashed_password)
            db.session.add(user)
            db.session.commit()
        
        response = self.app.post('/login', data=dict(
            email='newuser@example.com',
            password='newpassword123'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Profil', response.data)  # Sprawdzamy bardziej ogólną treść

    # Testowanie dostepu do zakladki "dieta" bez logowania
    def test_diet_access_without_login(self):
        response = self.app.get('/diet', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'zaloguj', response.data.lower())

    # Testowanie dostepu do zakladki "trening" bez logowania
    def test_training_access_without_login(self):
        response = self.app.get('/workout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'zaloguj', response.data.lower())

if __name__ == "__main__":
    unittest.main()

