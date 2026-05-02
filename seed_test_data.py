import os
from toon_db import ToonDB
from datetime import datetime, timedelta

if os.path.exists('data.toon'):
    os.remove('data.toon')

db = ToonDB()

# Add a test user
db.create_user("admin", "admin123", is_guest=False)
db.create_user("guest_user", "guest123", is_guest=True)

# Add famous quotes
quotes = [
    ("Be the change that you wish to see in the world.", "Mahatma Gandhi", "admin"),
    ("In three words I can sum up everything I've learned about life: it goes on.", "Robert Frost", "admin"),
    ("If you tell the truth, you don't have to remember anything.", "Mark Twain", "admin"),
    ("A friend is someone who knows all about you and still loves you.", "Elbert Hubbard", "guest_user"),
    ("To live is the rarest thing in the world. Most people exist, that is all.", "Oscar Wilde", "admin"),
    ("Darkness cannot drive out darkness: only light can do that. Hate cannot drive out hate: only love can do that.", "Martin Luther King Jr.", "guest_user"),
    ("Without music, life would be a mistake.", "Friedrich Nietzsche", "admin"),
    ("We accept the love we think we deserve.", "Stephen Chbosky", "admin"),
    ("It is better to be hated for what you are than to be loved for what you are not.", "Andre Gide", "guest_user")
]

base_date = datetime.now() - timedelta(days=1)
for i, (text, author, user) in enumerate(quotes):
    d_str = (base_date + timedelta(hours=i)).strftime("%Y-%m-%d %H:%M:%S")
    db.add_quote(text, author, user, d_str)

print("Database wiped and repopulated with famous quotes successfully!")
