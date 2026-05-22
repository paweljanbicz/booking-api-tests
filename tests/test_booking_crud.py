import requests

BASE_URL = "https://restful-booker.herokuapp.com"

def get_auth():
    resp = requests.post(f'{BASE_URL}/auth', json={
        "username": "admin",
        "password": "password123"
    })
    return resp.json()["token"]

def create_booking():
    resp = requests.post(f'{BASE_URL}/booking',
                         json={"firstname": "Eric",
                               "lastname": "Smith",
                               "totalprice": 351,
                               "depositpaid": False,
                               "bookingdates": {
                                   "checkin": "2025-02-15",
                                   "checkout": "2025-07-12"
                               },
                               "additionalneeds": "Breakfast"})
    return resp.json()["bookingid"]

class TestBookingCRUD:
    def test_get_booking_by_id(self):
        print(get_auth())

        resp = requests.get(f'{BASE_URL}/booking/12')

        assert resp.status_code == 200
        body = resp.json()
        assert body['firstname'] == "John"
        assert body['lastname'] == "Smith"
        assert body['totalprice'] == 111

    def test_get_all_bookings(self):
        resp = requests.get(f'{BASE_URL}/booking')

        assert resp.status_code == 200
        bookings = resp.json()
        assert len(bookings) > 0
        assert isinstance(bookings, list)
        assert 'bookingid' in bookings[0]

    def test_get_not_existing_booking_return_404(self):
        pass

    def test_create_booking_returns_201(self):
        pass

    def test_create_booking_missing_requirements_fails(self):
        pass

    def test_update_booking(self):
        pass

    def test_put_is_idempontet(self):
        pass

    def test_partial_booking_update_patch(self):
        pass

    def test_delete_booking(self):
        pass