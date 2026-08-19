import pytest
import time
from http import HTTPStatus
from conftest import DEFAULT_BOOKING_PAYLOAD


class TestBookingCRUD:
    @pytest.mark.smoke
    def test_get_booking_by_id(self, api_client, created_booking):
        resp = api_client.get_booking(created_booking)

        assert resp.status_code == HTTPStatus.OK
        body = resp.json()
        assert body['firstname'] == "Eric"
        assert body['lastname'] == "Smith"
        assert body['totalprice'] == 351

    @pytest.mark.regression
    def test_get_all_bookings(self, api_client):
        resp = api_client.get_all_bookings()

        assert resp.status_code == HTTPStatus.OK
        bookings = resp.json()
        assert len(bookings) > 0
        assert isinstance(bookings, list)
        assert 'bookingid' in bookings[0]

    @pytest.mark.negative
    def test_get_not_existing_booking_return_404(self, api_client):
        resp = api_client.get_booking(999999999999999)
        assert resp.status_code == HTTPStatus.NOT_FOUND

    @pytest.mark.regression
    def test_get_booking_by_filters(self, authenticated_client):
        unique_firstname = f"Eric{int(time.time())}"
        unique_lastname = f"Smith{int(time.time())}"
        checkout = "2025-07-12"
        booking_id = authenticated_client.create_booking({
            "firstname": unique_firstname,
            "lastname": unique_lastname,
            "totalprice": 351,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2025-02-15",
                "checkout": checkout,
            },
            "additionalneeds": "Breakfast",
        }).json()['bookingid']

        resp = authenticated_client.get_booking_by_filters(
            firstname=unique_firstname, lastname=unique_lastname, checkin="2025-02-14", checkout=checkout)
        booking_ids = [item['bookingid'] for item in resp.json()]
        assert booking_id in booking_ids
        authenticated_client.delete_booking(booking_id)

    @pytest.mark.negative
    def test_get_booking_by_checkin_filter_returns_empty_for_equal_date(self, authenticated_client):
        unique_firstname = f"Mark{int(time.time())}"
        unique_lastname = f"Newman{int(time.time())}"
        checkin = "2026-02-15"
        checkout = "2026-07-12"
        booking_id = authenticated_client.create_booking({
            "firstname": unique_firstname,
            "lastname": unique_lastname,
            "totalprice": 351,
            "depositpaid": False,
            "bookingdates": {
                "checkin": checkin,
                "checkout": checkout,
            },
            "additionalneeds": "Breakfast",
        }).json()['bookingid']

        resp = authenticated_client.get_booking_by_filters(
            firstname=unique_firstname, lastname=unique_lastname, checkin=checkin, checkout=checkout)
        assert resp.json() == []
        authenticated_client.delete_booking(booking_id)

    @pytest.mark.smoke
    def test_create_booking_returns_200(self, authenticated_client):
        resp = authenticated_client.create_booking(DEFAULT_BOOKING_PAYLOAD)
        assert resp.status_code == HTTPStatus.OK  # API restful-booker returns 200 instead of 201
        body = resp.json()
        assert isinstance(body['bookingid'], int)
        assert len(body) > 0
        assert body['booking']['firstname'] == DEFAULT_BOOKING_PAYLOAD['firstname']
        authenticated_client.delete_booking(body['bookingid'])

    @pytest.mark.negative
    @pytest.mark.parametrize('missing_field',
                             ["firstname", "lastname", "totalprice", "depositpaid"])
    def test_create_booking_missing_requirements_returns_500(self, api_client, missing_field):
        body = {k: v for k, v in DEFAULT_BOOKING_PAYLOAD.items() if k != missing_field}
        resp = api_client.create_booking(body)

        assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR  # API should return 400

    @pytest.mark.negative
    def test_create_booking_with_invalid_totalprice_string_sets_null(self, authenticated_client):
        invalid_payload = {**DEFAULT_BOOKING_PAYLOAD, 'totalprice': 'two hundred'}
        resp = authenticated_client.create_booking(invalid_payload)
        assert resp.status_code == HTTPStatus.OK
        assert resp.json()['booking']['totalprice'] is None

        authenticated_client.delete_booking(resp.json()['bookingid'])

    @pytest.mark.negative
    def test_create_booking_with_checkin_after_checkout_is_accepted(self, authenticated_client):
        check_in = '2026-04-01'
        check_out = '2026-03-01'
        payload = {**DEFAULT_BOOKING_PAYLOAD,
             "bookingdates":
                 {'checkin': check_in,
                  'checkout': check_out}
                   }

        resp = authenticated_client.create_booking(payload)
        booking_id = resp.json()['bookingid']
        booking_dates = resp.json()['booking']['bookingdates']

        assert resp.status_code == HTTPStatus.OK    # BUG: should return 400 BAD_REQUEST
        assert booking_dates['checkin'] == check_in
        assert booking_dates['checkout'] == check_out

        authenticated_client.delete_booking(booking_id)

    @pytest.mark.smoke
    def test_update_booking(self, authenticated_client, created_booking):
        updated = {
            "firstname": "Adam",
            "lastname": "Jonson",
            "totalprice": 999,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2026-02-15",
                "checkout": "2027-01-01"
            },
            "additionalneeds": "None"
        }

        resp = authenticated_client.update_booking(created_booking, updated)
        body = resp.json()
        assert resp.status_code == HTTPStatus.OK
        assert body['firstname'] == "Adam"
        assert body['lastname'] == "Jonson"
        assert body['totalprice'] == 999
        assert body['depositpaid'] is False

    @pytest.mark.negative
    def test_update_booking_without_auth(self, api_client, authenticated_client):
        booking_id = api_client.create_booking(DEFAULT_BOOKING_PAYLOAD).json()['bookingid']
        updated = {
            "firstname": "Adam",
            "lastname": "Jonson",
            "totalprice": 999,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2026-02-15",
                "checkout": "2027-01-01"
            },
            "additionalneeds": "None"
        }

        resp = api_client.update_booking(booking_id, updated, is_auth=False)
        assert resp.status_code == HTTPStatus.FORBIDDEN
        authenticated_client.delete_booking(booking_id)

    @pytest.mark.negative
    def test_update_non_existing_booking_returns_405(self, authenticated_client):
        updated = {
            "firstname": "Adam",
            "lastname": "Jonson",
            "totalprice": 999,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2026-02-15",
                "checkout": "2027-01-01"
            },
            "additionalneeds": "None"
        }
        resp = authenticated_client.update_booking(999999999999999, updated)
        assert resp.status_code == HTTPStatus.METHOD_NOT_ALLOWED  #API should return 404 for a non-existent resource

    @pytest.mark.regression
    def test_put_is_idempotent(self, authenticated_client, created_booking):
        updated = {
            "firstname": "Adam",
            "lastname": "Jonson",
            "totalprice": 999,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2026-02-15",
                "checkout": "2027-01-01"
            },
            "additionalneeds": "None"
        }

        resp1 = authenticated_client.update_booking(created_booking, updated)
        resp2 = authenticated_client.update_booking(created_booking, updated)
        resp3 = authenticated_client.update_booking(created_booking, updated)
        assert resp1.status_code == resp2.status_code == resp3.status_code == HTTPStatus.OK
        assert resp1.json() == resp2.json() == resp3.json()

    @pytest.mark.regression
    def test_partial_booking_update_patch(self, authenticated_client, created_booking):
        resp = authenticated_client.partial_update_booking(created_booking, {"firstname": "Adam"})
        assert resp.status_code == HTTPStatus.OK
        assert resp.json()['firstname'] == "Adam"

    @pytest.mark.negative
    def test_partial_booking_update_patch_without_auth(self, api_client, authenticated_client):
        booking_id = api_client.create_booking(DEFAULT_BOOKING_PAYLOAD).json()['bookingid']
        resp = api_client.partial_update_booking(booking_id, {"firstname": "Adam"}, is_auth=False)
        assert resp.status_code == HTTPStatus.FORBIDDEN
        authenticated_client.delete_booking(booking_id)

    @pytest.mark.regression
    def test_delete_booking_with_authorized_client(self, authenticated_client):
        booking_id = authenticated_client.create_booking(DEFAULT_BOOKING_PAYLOAD).json()['bookingid']
        resp = authenticated_client.delete_booking(booking_id)
        assert resp.status_code == HTTPStatus.CREATED  # API should return 204 status code

        get_resp = authenticated_client.get_booking(booking_id)
        assert get_resp.status_code == HTTPStatus.NOT_FOUND

    @pytest.mark.negative
    def test_delete_booking_without_auth(self, api_client):
        booking_id = api_client.create_booking(DEFAULT_BOOKING_PAYLOAD).json()['bookingid']
        resp = api_client.delete_booking(booking_id, is_auth=False)
        assert resp.status_code == HTTPStatus.FORBIDDEN

    @pytest.mark.negative
    def test_delete_non_existing_booking_returns_405(self, authenticated_client):
        resp = authenticated_client.delete_booking(999999999999999)
        assert resp.status_code == HTTPStatus.METHOD_NOT_ALLOWED  #API should return 404 for a non-existent resource
