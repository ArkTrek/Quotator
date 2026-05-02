import toon

data = {
    "users": {"admin": {"password": "123", "is_guest": False}},
    "quotes": [{"id": "q1", "text": "hello", "author": "me", "date": "2026", "likes": []}]
}

try:
    encoded = toon.encode(data)
    print("Encoded:", encoded)
    decoded = toon.decode(encoded)
    print("Decoded:", decoded)
except Exception as e:
    print("Error:", e)
