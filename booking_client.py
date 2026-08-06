import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BOOKING_API_BASE_URL", "https://restful-booker.herokuapp.com")


class BookingClient:
    def __init__(self, base_url: str = BASE_URL) -> None:
        self.base_url = base_url
        self.session = requests.Session()
        self._token: str | None = None

    def authenticate(self, username: str = os.getenv("BOOKING_API_USERNAME", "admin"),
                     password: str = os.getenv("BOOKING_API_PASSWORD", "password123")) -> str:
        resp = self.session.post(f'{self.base_url}/auth', json={
            "username": username,
            "password": password
        })
        self._token = resp.json()["token"]
        return self._token

    def _auth_headers(self) -> dict[str, str]:
        if self._token is None:
            raise RuntimeError("No auth token set - call authenticate() first")
        return {"Cookie": f"token={self._token}"}

    def create_booking(self, payload: dict[str, Any]) -> requests.Response:
        return self.session.post(f'{self.base_url}/booking', json=payload)

    def get_booking(self, booking_id: int) -> requests.Response:
        return self.session.get(f'{self.base_url}/booking/{booking_id}')

    def get_all_bookings(self) -> requests.Response:
        return self.session.get(f'{self.base_url}/booking')

    def update_booking(self, booking_id: int, payload: dict[str, Any]) -> requests.Response:
        return self.session.put(f'{self.base_url}/booking/{booking_id}',
                                json=payload,
                                headers=self._auth_headers())

    def partial_update_booking(self, booking_id: int, payload: dict[str, Any]) -> requests.Response:
        return self.session.patch(f'{self.base_url}/booking/{booking_id}',
                                  json=payload,
                                  headers=self._auth_headers())

    def delete_booking(self, booking_id: int, is_auth: bool = True) -> requests.Response:
        headers = self._auth_headers() if is_auth else {}
        return self.session.delete(f'{self.base_url}/booking/{booking_id}',
                                   headers=headers)

