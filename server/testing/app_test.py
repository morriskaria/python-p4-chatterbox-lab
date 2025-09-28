#!/usr/bin/env python3

import pytest
from app import app
from models import db, Message

class TestApp:
    """Test cases for Chatterbox API"""
    
    @pytest.fixture(autouse=True)
    def setup_database(self):
        """Set up the database for each test"""
        with app.app_context():
            # Clear existing data
            db.session.rollback()
            Message.query.delete()
            
            # Create test messages
            messages = [
                Message(body="Test message 1", username="user1"),
                Message(body="Test message 2", username="user2"),
                Message(body="Test message 3", username="user3")
            ]
            db.session.add_all(messages)
            db.session.commit()
            
            yield
            
            # Clean up after test
            db.session.rollback()

    def test_has_correct_columns(self):
        """has columns for message body, username, and creation time."""
        with app.app_context():
            message = Message.query.first()
            
            assert hasattr(message, 'id')
            assert hasattr(message, 'body')
            assert hasattr(message, 'username')
            assert hasattr(message, 'created_at')

    def test_returns_list_of_json_objects_for_all_messages(self):
        """returns a list of JSON objects for all messages in the database."""
        with app.app_context():
            response = app.test_client().get('/messages')
            messages = Message.query.all()
            
            assert response.status_code == 200
            
            json_data = response.get_json()
            assert isinstance(json_data, list)
            assert len(json_data) == len(messages)

    def test_creates_new_message_in_database(self):
        """creates a new message in the database."""
        with app.app_context():
            initial_count = Message.query.count()
            
            response = app.test_client().post(
                '/messages',
                json={
                    'body': 'This is a test message',
                    'username': 'testuser'
                }
            )
            
            final_count = Message.query.count()
            assert final_count == initial_count + 1

    def test_returns_data_for_newly_created_message_as_json(self):
        """returns data for the newly created message as JSON."""
        response = app.test_client().post(
            '/messages',
            json={
                'body': 'This is a test message',
                'username': 'testuser'
            }
        )
        
        assert response.status_code == 201
        
        json_data = response.get_json()
        assert json_data['body'] == 'This is a test message'
        assert json_data['username'] == 'testuser'
        assert 'id' in json_data
        assert 'created_at' in json_data

    def test_updates_body_of_message_in_database(self):
        """updates the body of a message in the database."""
        with app.app_context():
            # Get the first message
            message = Message.query.first()
            message_id = message.id
            
            response = app.test_client().patch(
                f'/messages/{message_id}',
                json={
                    'body': 'Test Message Updated'
                }
            )
            
            # Check that the message was updated in the database
            updated_message = Message.query.get(message_id)
            assert updated_message.body == 'Test Message Updated'

    def test_returns_data_for_updated_message_as_json(self):
        """returns data for the updated message as JSON."""
        with app.app_context():
            # Get the first message
            message = Message.query.first()
            message_id = message.id
            
            response = app.test_client().patch(
                f'/messages/{message_id}',
                json={
                    'body': 'Test Message Updated'
                }
            )
            
            json_data = response.get_json()
            
            assert response.status_code == 200
            assert json_data['body'] == 'Test Message Updated'
            assert json_data['username'] == message.username
            assert 'created_at' in json_data

    def test_deletes_message_from_database(self):
        """deletes the message from the database."""
        with app.app_context():
            initial_count = Message.query.count()
            message = Message.query.first()
            message_id = message.id
            
            response = app.test_client().delete(f'/messages/{message_id}')
            
            final_count = Message.query.count()
            assert final_count == initial_count - 1
            
            # Verify the specific message is gone
            deleted_message = Message.query.get(message_id)
            assert deleted_message is None