![API Tests](https://github.com/paweljanbicz/booking-api-tests/actions/workflows/tests.yml/badge.svg)
## Booking API Tests
Automated API test suite for [Restful-Booker](https://restful-booker.herokuapp.com/apidoc/index.html) — a deliberately buggy booking API used for API testing practice.
### Tests Coverage    
- CRUD operations — create, read, update, delete bookings
  - smoke: core create/read/update flow
  - negative: missing fields, non-existent booking, unauthorized delete
  - regression: idempotent update, partial update, authorized delete, gathering all bookings
  

### Tech stack  
- Python 3.x  
- pytest  
- requests
- python-dotenv


### How to run
```bash
git clone https://github.com/paweljanbicz/booking-api-tests.git
cd booking-api-tests
pip install -r requirements.txt
copy .env.example .env
pytest              # full suite
pytest -m smoke     # quick smoke check
```

### Project structure
``` booking-api-tests/
├── tests/
│   ├── test_booking_crud.py
├── .env.example
├── booking_client.py
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```
Notes:  
API resets every 10 minutes to its default state (10 pre-loaded records).
