#testing user regestration API endpoint
#importing unittest
#importing requests

import unittest
import requests

class TestUserRegistrationAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://localhost:5000'

#Testing if user can successfuly register
    def test_register_success(self):
        payload = {'username': 'Eren', 'password': 'Eren@1234'}
        response = requests.post(self.base_url + '/register', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertTrue('message' in response.json())
        self.assertEqual(response.json()['message'], 'User registered successfully')

#Testing if user can login via missing password or username
    def test_register_missing_data(self):
        payload = {'username': 'Eren'}
        response = requests.post(self.base_url + '/register', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('message' in response.json())
        self.assertEqual(response.json()['message'], 'Missing username or password')

#Testing if user already existed or not.
    def test_register_duplicate_username(self):
        payload = {'username': 'Eren', 'password': 'Eren@1234'}
        response1 = requests.post(self.base_url + '/register', json=payload)
        response2 = requests.post(self.base_url + '/register', json=payload)
        self.assertEqual(response2.status_code, 400)
        self.assertTrue('message' in response2.json())
        self.assertEqual(response2.json()['message'], 'Username already exists')


