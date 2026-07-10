import requests

BASE_URL = "https://restful-booker.herokuapp.com"

class BookingClient:
    def __init__(self, base_url= BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self._token = None

    def authenticate(self, username= "admin", password = "password123"):
        resp = self.session.post(f'{self.base_url}/auth', json={
            "username": username,
            "password": password
        })
        self._token = resp.json()["token"]
        return self._token

    def create_booking(self, payload):
        return self.session.post(f'{self.base_url}/booking', json=payload)

    def get_booking(self, booking_id):
        return self.session.get(f'{self.base_url}/booking/{booking_id}')
