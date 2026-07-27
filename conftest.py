from typing import Any
from booking_client import BookingClient
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


@pytest.fixture(scope="session")
def api_client():
    return BookingClient()


@pytest.fixture(scope="session")
def authenticated_client(api_client):
    api_client.authenticate()
    return api_client


@pytest.fixture()
def created_booking(authenticated_client):
    booking_id = authenticated_client.create_booking(DEFAULT_BOOKING_PAYLOAD).json()['bookingid']
    yield booking_id
    authenticated_client.delete_booking(booking_id)
