import unittest 
from base import BaseTestCase 
from app import app, db, bcrypt
from app.models import Users 
from app.forms import LoginForm
from flask_login import current_user 

class TestLogin(BaseTestCase):

    def test_index(self):
        response = self.client.get("/login", content_type="html/text")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_correct_login(self):
        with self.client:
            self.client.get("/login", follow_redirects=True)
            response = self.client.post("/login", data=dict(username='jeff', password='123456'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"You just logged in as jeff!", response.data)
            self.assertTrue(current_user.username == 'jeff')
            self.assertTrue(current_user.id == 1)
            self.assertTrue(current_user.is_active)

    def test_logout(self):
        with self.client:
            response = self.client.post("/login", data=dict(username='jeff', password='123456'), follow_redirects=True)
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b"You just successfully logged out", response.data)
            self.assertFalse(current_user.is_active)

    def test_logout_login_required(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b"You have to login first", response.data)

    def test_validate_success_login_form(self):
        # Ensure correct data validates.
        form = LoginForm(username='jeff', password='123456')
        self.assertTrue(form.validate())

    def test_validate_invalid_email_format(self):
        # Ensure invalid username throws error
        form = LoginForm(username='12', password='examp')
        self.assertFalse(form.validate())

    def test_check_password(self):
        # Ensure given password is correct after unhashing.
        user = Users.query.filter_by(username='jeff').first()
        self.assertTrue(
            bcrypt.check_password_hash(user.password, '123456'))
        self.assertFalse(bcrypt.check_password_hash(user.password, 'foobar'))

    def test_validate_invalid_password(self):
        # Ensure user can't login when the pasword is incorrect.
        with self.client:
            self.client.get('/logout', follow_redirects=True)
            response = self.client.post('/login', data=dict(
                username='admin@admin.com', password='foo_bar'
            ), follow_redirects=True)
        self.assertIn(b'<strong>Invalid password.</strong> Please try again.', response.data)

    def test_register(self):
        # Ensure about route behaves correctly.
        response = self.client.get('/', follow_redirects=True)
        self.assertIn(b'Sign up', response.data)

    def test_student_registration(self):
        # Ensure registration behaves correctly.
        with self.client:
            response = self.client.post(
                '/',
                data=dict(
                    username='test@tester.com',
                    password='testing',
                    confirm='testing',
                    accept_tos=True

                ),
                follow_redirects=True
            )
            self.assertIn(b'You have just signup up congrats!',response.data)
            self.assertTrue(current_user.username == 'test@tester.com')
            self.assertTrue(current_user.is_authenticated)
            self.assertTrue(current_user.is_active)
            self.assertEqual(response.status_code, 200)

    def test_student_registration_unique_username(self):
        # Ensure a student cannot register with a duplicate username.
        with self.client:
            response = self.client.post(
                '/',
                data=dict(
                    username='jeff',
                    password='student',
                    confirm='student',
                    accept_tos=True
                ),
                follow_redirects=True
            )
            self.assertIn(
                b'That username already exists',
                response.data
            )
            self.assertTemplateUsed('signup.html')
            self.assertEqual(response.status_code, 200)

