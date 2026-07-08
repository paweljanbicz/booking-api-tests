from typing import Any
import requests
import pytest

DEFAULT_BOOKING_PAYLOAD: dict[str, Any] = {
    "firstname": "Eric",
    "lastname": "Smith",
    "totalprice": 351,
    "depositpaid": False,
    "bookingdates": {
        "checkin": "2025-02-15",
        "checkout": "2025-07-12",
    },
    "additionalneeds": "Breakfast",
}

BASE_URL = "https://restful-booker.herokuapp.com"

@pytest.fixture(scope="session")
def auth_token():
    resp = requests.post(f'{BASE_URL}/auth', json={
        "username": "admin",
        "password": "password123"
    })
    return resp.json()["token"]

def create_test_booking():
    resp = requests.post(f'{BASE_URL}/booking', json=DEFAULT_BOOKING_PAYLOAD)
    return resp.json()['bookingid']

@pytest.fixture()
def created_booking(auth_token):
    booking_id = create_test_booking()
    yield booking_id
    requests.delete(f'{BASE_URL}/booking/{booking_id}', headers={"Cookie": f"token={auth_token}"})