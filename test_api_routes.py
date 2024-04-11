import unittest
from app import app

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_landing_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        print("Successfully accessed landing page")

    def test_get_planets(self):
        response = self.app.get('/planets')
        self.assertEqual(response.status_code, 200)
        print("Successfully accessed planets route")

    def test_get_systems(self):
        response = self.app.get('/systems')
        self.assertEqual(response.status_code, 200)
        print("Successfully accessed systems route")

    def test_get_resources(self):
        response = self.app.get('/resources')
        self.assertEqual(response.status_code, 200)
        print("Successfully accessed resources route")

    def test_get_planet_resources(self):
        response = self.app.get('/planet_resources')
        self.assertEqual(response.status_code, 200)
        print("Successfully accessed planet_resources route")

if __name__ == '__main__':
    unittest.main()
