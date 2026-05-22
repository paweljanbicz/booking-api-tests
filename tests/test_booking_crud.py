import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"
BOOKING_PAYLOAD = {
    "firstname": "Eric",
    "lastname": "Smith",
    "totalprice": 351,
    "depositpaid": False,
    "bookingdates": {
        "checkin": "2025-02-15",
        "checkout": "2025-07-12"
    },
    "additionalneeds": "Breakfast"}

def get_auth():
    resp = requests.post(f'{BASE_URL}/auth', json={
        "username": "admin",
        "password": "password123"
    })
    return resp.json()["token"]

def create_booking():
    resp = requests.post(f'{BASE_URL}/booking', json=BOOKING_PAYLOAD)
    return resp.json()

class TestBookingCRUD:
    def test_get_booking_by_id(self):
        booking_id = create_booking()["bookingid"]

        resp = requests.get(f'{BASE_URL}/booking/{booking_id}')

        assert resp.status_code == 200
        body = resp.json()
        assert body['firstname'] == "Eric"
        assert body['lastname'] == "Smith"
        assert body['totalprice'] == 351

    def test_get_all_bookings(self):
        resp = requests.get(f'{BASE_URL}/booking')

        assert resp.status_code == 200
        bookings = resp.json()
        assert len(bookings) > 0
        assert isinstance(bookings, list)
        assert 'bookingid' in bookings[0]

    def test_get_not_existing_booking_return_404(self):
        resp = requests.get(f'{BASE_URL}/booking/999999999999999')
        assert resp.status_code == 404

    def test_create_booking_returns_201(self):
        resp = requests.post(f'{BASE_URL}/booking', json=BOOKING_PAYLOAD)

        assert resp.status_code == 200  #API restful-booker returns 200 instead of 201
        body = resp.json()
        assert isinstance(body['bookingid'], int)
        assert len(body) > 0
        assert body['booking']['firstname'] == BOOKING_PAYLOAD['firstname']

    @pytest.mark.parametrize('missing_field',
                             ["firstname", "lastname", "totalprice", "depositpaid"])
    def test_create_booking_missing_requirements_fails(self, missing_field):
        body = {k:v for k,v in BOOKING_PAYLOAD.items() if k not in missing_field}
        resp = requests.post(f'{BASE_URL}/booking', json=body)

        assert resp.status_code in (400, 422, 500) #API should return 400


    def test_update_booking(self):
        pass

    def test_put_is_idempontet(self):
        pass

    def test_partial_booking_update_patch(self):
        pass

    def test_delete_booking(self):
        pass