import unittest
from base import BaseTestCase
from app import db
from app.models import AsciiArt
from flask_login import current_user

class TestFrontPage(BaseTestCase):

    def test_front(self):
        with self.client:
            self.client.get("/login", follow_redirects=True)
            response = self.client.post("/login", data=dict(username='jeff', password='123456'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"/ascii/", response.data)
            self.assertIn(b"paste your ascii artwork here...", response.data)

    def test_art_add_new_success(self):
        with self.client:
            self.client.get("/login", follow_redirects=True)
            response = self.client.post("/login", data=dict(username='jeff', password='123456'), follow_redirects=True)
            response1 = self.client.post("/ascii", data=dict(title="title", art="art"), follow_redirects=True)
            self.assertEqual(response1.status_code, 200)
            self.assertIn(b"You just posted some <strong>ascii</strong> artwork!", response1.data)

    def test_art_error(self):
        with self.client:
            self.client.get("/login", follow_redirects=True)
            response = self.client.post("/login", data=dict(username='jeff', password='123456'), follow_redirects=True)
            response1 = self.client.post("/ascii", data=dict(title="",art=""), follow_redirects=True)
            self.assertIn(b"Hey, you need a title.",response1.data)
            self.assertIn(b"Hey buddy, you need to paste in some ascii artwork.",response1.data)

    def test_art_delete_status(self):
        with self.client:
            response = self.client.post("/login", data=dict(username='jeff', password='123456'), follow_redirects=True)
            response = self.client.get("/1/delete", content_type="html/text")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"You sure you want to delete <u>test title</u>?", response.data)

    def test_adoptors_delete_post(self):
        with self.client:
            response = self.client.post("/login", data=dict(username='jeff', password='123456'), follow_redirects=True)
            response = self.client.post("/1/delete", follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Just deleted <u>test title</u>", response.data)

    def test_art_edit_status(self):
        with self.client:
            response = self.client.post("/login", data=dict(username='jeff', password='123456'), follow_redirects=True)
            response = self.client.get("/1/edit", content_type="html/text")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"/edit/", response.data)

    def test_art_edit_post(self):
        with self.client:
            response = self.client.post("/login", data=dict(username='jeff', password='123456'), follow_redirects=True)
            response = self.client.post("/1/edit", data=dict(title="Editname",art="edit art"), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Successful Edit of <strong>Editname</strong>", response.data)

    def test_ajax_status(self):
        with self.client:
            response = self.client.post("/login", data=dict(username='jeff', password='123456'), follow_redirects=True)
            response = self.client.get("/ajax", content_type="html/text")
            self.assertEqual(response.status_code,200)
            self.assertIn(b"Where do you want to live?",response.data)

    def test_puppy_api_status(self):
        with self.client:
            response = self.client.post("/login", data=dict(username='jeff', password='123456'), follow_redirects=True)
            response = self.client.get("/puppy-api-example", content_type="html/text")
            self.assertEqual(response.status_code,200)
            self.assertIn(b"This page was made to show that I can create and use api's.",response.data)

    def test_ascii_db(self):
        test = AsciiArt.query.filter_by(id=1).one()
        self.assertIn(b"test title",test.title)
        self.assertIn(b"test art",test.art)
        assert 55.555 == test.lat
        assert 55.555 == test.lon
        artwork = AsciiArt(title="my title", art="my art")
        db.session.add(artwork)
        db.session.commit()
        test2 = AsciiArt.query.filter_by(title="my title").one()
        self.assertIn(b"my title", test2.title)
        self.assertIn(b"my art", test2.art)