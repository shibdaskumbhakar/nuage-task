from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
import json
from django.contrib.auth import get_user_model

User = get_user_model()


client = Client()



class LoginREgistrationTest(TestCase):
    """ Test module for Login REgistration API """

    def setUp(self):

        self.user = User(email="shibdas2@gmail.com")
        password = 'admin@123'
        self.user.set_password(password)
        self.user.save()


    def test_login(self):
        self.payload = {
            'email': self.user.email,
            'password': 'admin@123'
        }
        response = client.post(
            reverse('accounts:token_obtain_pair'),
            data=json.dumps(self.payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_registration(self):
        payload = {
            "name":"shibdas",
            "email":"shibdas10@gmail.com",
            "phone":"9609572412",
            "password":"12345678",
        }
        response = client.post(
            reverse('accounts:signup'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)