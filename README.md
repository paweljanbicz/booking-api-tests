## Booking API Tests
Automated API test suite for Restful-Booker — a deliberately buggy booking API used for API testing practice.

###  Tests covers  
- Authentication — token generation, invalid credentials  
- CRUD operations — create, read, update, delete bookings  
- Validation — response schemas, status codes, error handling  
  

### Tech stack  
- Python 3.x  
- pytest  
- requests


### How to run
```bash
git clone https://github.com/paweljanbicz/booking-api-tests.git
cd booking-api-tests
pip install -r requirements.txt
pytest
```

### Project structure
``` booking-api-tests/
├── tests/
│   ├── test_auth.py
│   ├── test_booking_crud.py
│   ├── test_booking_filter.py
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```
Notes:  
API resets every 10 minutes to its default state (10 pre-loaded records).
