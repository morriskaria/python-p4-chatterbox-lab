#!/usr/bin/env python3

from app import app
from models import db, Message

with app.app_context():
    # Clear existing data
    Message.query.delete()
    
    # Seed messages
    messages = [
        Message(
            body="Hello, world!",
            username="user1"
        ),
        Message(
            body="This is a test message",
            username="user2"
        ),
        Message(
            body="Chatterbox is working!",
            username="user3"
        ),
        Message(
            body="Another message for testing",
            username="user1"
        ),
        Message(
            body="Final test message",
            username="user2"
        )
    ]
    
    db.session.add_all(messages)
    db.session.commit()
    print("Database seeded successfully!")