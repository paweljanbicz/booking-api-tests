import requests

BASE_URL = "https://restful-booker.herokuapp.com"

def get_auth():
    resp = requests.post(f'{BASE_URL}/auth', json={
        "username": "admin",
        "password": "password123"
    })
    return resp.json()["token"]

class TestBookingCRUD:
    def test_get_booking_by_id(self):
        resp = requests.get(f'{BASE_URL}/booking/1')

        assert resp.status_code == 200
        body = resp.json()
        assert body['firstname'] == "Eric"
        assert body['lastname'] == "Smith"
        assert body['totalprice'] == 351

    def test_get_all_bookings(self):
        pass

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