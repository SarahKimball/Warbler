import unittest
from models import db, Message
from app import app

# Define a test case for the Message model
class MessageModelTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        """Tear down the test environment."""
        db.session.remove()
        db.drop_all()

    def test_create_message(self):
        """Test creating a new message."""
        # Create a new message
        message = Message(text='Hello, World!')
        db.session.add(message)
        db.session.commit()

        # Retrieve the message from the database
        retrieved_message = Message.query.first()

        # Assert that the retrieved message is not None
        self.assertIsNotNone(retrieved_message)

        # Assert that the retrieved message has the correct text
        self.assertEqual(retrieved_message.text, 'Hello, World!')

    def test_delete_message(self):
        """Test deleting a message."""
        # Create a new message
        message = Message(text='To be deleted')
        db.session.add(message)
        db.session.commit()

        # Delete the message
        db.session.delete(message)
        db.session.commit()

        # Try to retrieve the deleted message from the database
        retrieved_message = Message.query.get(message.id)

        # Assert that the retrieved message is None
        self.assertIsNone(retrieved_message)

# Run the tests
if __name__ == '__main__':
    unittest.main()
