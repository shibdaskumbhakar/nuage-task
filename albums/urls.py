from django.urls import path
from .views import GetAllAlbums, GetAlbumView, GetAlbumsTracks, GetAllNewReleasesAlbum

"""
Urls for albums 
"""


urlpatterns = [
    path('get-album/<int:album_id>', GetAlbumView.as_view(), name='get-album'),
    path('get-several-albums', GetAllAlbums.as_view(), name='get-all-albums'),
    path('get-albums-track/<int:album_id>', GetAlbumsTracks.as_view(), name='get-album-track'),
    path('get-new-relese-album', GetAllNewReleasesAlbum.as_view(), name='get-new-relese-album')
]
