# server/seed.py
from app import app
from models import db, Message

def seed_database():
    with app.app_context():
        # Clear existing data
        db.session.query(Message).delete()
        
        # Add sample messages
        messages = [
            Message(body="Hello 👋", username="Liza"),
            Message(body="Hi!", username="Duane"),
            Message(body="Hey there!", username="Akiko"),
            Message(body="What's up?", username="Bob"),
            Message(body="Nice to see you!", username="Alice")
        ]
        
        db.session.add_all(messages)
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()