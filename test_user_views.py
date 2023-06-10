import unittest
from models import db, User
from app import app

# Define a test case for the user views
class UserViewsTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down the test environment."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_users(self):
        """Test getting all users."""
        # Create some sample users
        user1 = User(username='user1')
        user2 = User(username='user2')
        db.session.add_all([user1, user2])
        db.session.commit()

        # Make a GET request to the users endpoint
        response = self.client.get('/users')

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the response data contains the correct users
        data = response.get_json()
        self.assertEqual(len(data['users']), 2)
        self.assertEqual(data['users'][0]['username'], 'user1')
        self.assertEqual(data['users'][1]['username'], 'user2')

    def test_create_user(self):
        """Test creating a new user."""
        # Make a POST request to create a new user
        response = self.client.post('/users', json={'username': 'newuser'})

        # Assert that the response status code is 201 (Created)
        self.assertEqual(response.status_code, 201)

        # Assert that the user is created in the database
        with app.app_context():
            user = User.query.filter_by(username='newuser').first()
            self.assertIsNotNone(user)

    def test_delete_user(self):
        """Test deleting a user."""
        # Create a user to be deleted
        user = User(username='tobedeleted')
        db.session.add(user)
        db.session.commit()

        # Make a DELETE request to delete the user
        response = self.client.delete(f'/users/{user.id}')

        # Assert that the response status code is 204 (No Content)
        self.assertEqual(response.status_code, 204)

        # Assert that the user is deleted from the database
        with app.app_context():
            deleted_user = User.query.get(user.id)
            self.assertIsNone(deleted_user)

# Run the tests
if __name__ == '__main__':
    unittest.main()
