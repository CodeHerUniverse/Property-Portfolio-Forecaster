import unittest
from unittest import TestCase
from Property_Portfolio_Forecaster_app import app  # Importing the Flask app to be tested

# Define the TestFlaskApp class
class TestFlaskApp(unittest.TestCase):

    # setUp method runs before each test case, initialises the test client
    def setUp(self):

        # Creates a test client for the app to simulate HTTP requests
        self.client = app.test_client()

        # Set testing to True, so Flask behaves differently for tests
        self.client.testing = True


    # Test the index route ("/") to ensure it's accessible and returns the correct response
    def test_index(self):

        # Simulate a GET request to the endpoint ("/")
        response = self.client.get('/')

        # Assert the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Assert the response contains the expected welcome message
        self.assertIn(b"Welcome to the Property Portfolio & Forecaster!", response.data)


    # Test the /all_properties endpoint to ensure it returns the correct data
    def test_get_all_properties(self):

        # Simulate a GET request to the /all_properties endpoint
        response = self.client.get('/all_properties')

        # Assert the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Assert the response contains "Property ID" in the data
        self.assertIn(b"Property ID", response.data)


    # Test the /properties_by_bedroom_nr/2 endpoint to return properties with 2 bedrooms
    def test_get_properties_by_bedroom_number(self):

        # Simulate a GET request to the /properties_by_bedroom_nr/2 endpoint
        response = self.client.get('/properties_by_bedroom_nr/2')

        # Assert the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Assert the response contains "Number of Bedrooms" in the data
        self.assertIn(b"Number of Bedrooms", response.data)


    # Test the /renovations_tracker/999 endpoint for a non-existent property ID (1000)
    def test_get_renovations_tracker_invalid_property(self):

        # Simulate a GET request to the /renovations_tracker/1000 endpoint for a non-existent property
        response = self.client.get('/renovations_tracker/1000')

        # Assert that the response status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)

        # Assert that the response contains the expected error message
        self.assertIn(b"No renovations found for property ID", response.data)


# Check to see if this script is being run directly or being imported as a module
if __name__ == '__main__':
    # Run all the test cases
    unittest.main()