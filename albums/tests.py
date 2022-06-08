from django.test import TestCase, Client
from .models import Artist
from django.urls import reverse
from rest_framework import status
import json
from django.contrib.auth import get_user_model

User = get_user_model()


client = Client()


class ArtistModelTest(TestCase):
    """ Test module for Artist model """

    def setUp(self):
        Artist.objects.create(
            artist_name='Arijit Singh', short_bio='Very Good Singer', popularity=100)
        Artist.objects.create(
            artist_name='Shaan', short_bio='Very Good Singer', popularity=100)

    def test_artist_name(self):
        shaan_artist = Artist.objects.get(artist_name='Shaan')
        self.assertEqual(
            shaan_artist.artist_name, "Shaan")
        

class AllAlbumTest(TestCase):
    """ Test module for GET all albums API """

    def setUp(self):

        self.user = User(email="shibdas1@gmail.com")
        password = 'admin@123'
        self.user.set_password(password)
        self.user.save()


        self.payload = {
            'email': self.user.email,
            'password': password
        }
        response = client.post(
            reverse('accounts:token_obtain_pair'),
            data=json.dumps(self.payload),
            content_type='application/json'
        )
        self.access_token = response.json()['access']


    def test_get_all_albums(self):
        response = self.client.get(
            reverse('get-all-albums'),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_albums_method_not_allowed(self):
        response = self.client.put(
            reverse('get-all-albums'),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_new_realease_album(self):
        response = self.client.get(
            reverse('get-new-relese-album'),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_new_realease_album_method_not_allowed(self):
        response = self.client.put(
            reverse('get-new-relese-album'),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
