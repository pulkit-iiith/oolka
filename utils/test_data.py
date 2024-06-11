event_data = {
        "name": "Test Event",
        "date": "2023-12-31",
        "location": "Test Location",
        "total_tickets": 100,
        "ticket_price": 50,
        "event_type": "music festival"
    }

booking_data = {
    "tickets": 1,
    "payment_source": "test source"
}

tickets_not_available_data = {
    "tickets": 101,
    "payment_source": "test source"
}

user_data_admin = {
    "username": "testUser",
    "email": "test@yopmail.com",
    "is_admin": True,
    "password": "password"
}

user_data_not_admin = {
    "username": "testUser",
    "email": "test@yopmail.com",
    "is_admin": False,
    "password": "password"
}

headers = {
    "Authorization": "test token"
}