from rest_framework.views import APIView
from .models import Album, Track
from .serializers import AlbumSerializer, AlbumsTrackSerializer
from accounts.utils import ResponseInfo
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime, timedelta, date
import pytz
from .utils import CustomPaginator
import time
import logging
from drf_yasg.utils import swagger_auto_schema


logger = logging.getLogger(__name__)

class GetAlbumView(APIView):
    """
    Get a Single album
    """
    def __init__(self):
        self.response = ResponseInfo().response

    def get_album(self, album_id):
        try:
            obj = Album.objects.get(id=album_id)
            return obj
        except Album.DoesNotExist:
            return False
    
    @swagger_auto_schema(
        operation_description="This API used for get a single album"
    )
    def get(self, request, album_id):
        logger.info("GET request arrived for 'get-album' at " + str(time.strftime('%X %x %Z')))
        album_obj = self.get_album(album_id)
        if album_obj:
            try:
                serializer = AlbumSerializer(album_obj, context={'request': request})
                self.response['data'] = serializer.data
                self.response['message'] = 'Successfully Get the Album'
            except Exception as e:
                logger.error(f"GET request for 'get-album' failed as {e}")
                self.response['message'] = 'Something went wrong'
                self.response['status'] = status.HTTP_400_BAD_REQUEST
        else:
            logger.info(f"GET request for 'get-album' failed as No Album Found with {album_id} id ")
            self.response['message'] = 'No Album Found with this id'
            self.response['status'] = status.HTTP_200_OK
        return Response(self.response, status=self.response['status'])

    @swagger_auto_schema(
        operation_description="This API used for delete a single album"
    )
    def delete(self, request, album_id):
        album_obj = self.get_album(album_id)
        if album_obj:
            album_obj.delete()
            self.response['message'] = 'Album Successfully Deleted'
            self.response['status'] = status.HTTP_200_OK
        else:
            self.response['message'] = 'No Album Found'
        return Response(self.response, status=self.response['status'])
        

class GetAllAlbums(APIView):
    """
    Get all albums data
    """
    def __init__(self):
        self.response = ResponseInfo().response

    def get_all_albums(self):
        return Album.objects.filter(active=True)

    @swagger_auto_schema(
        operation_description="This API used for get all album"
    )
    def get(self, request):
        albums = self.get_all_albums()
        serializer = AlbumSerializer(albums, many=True, context={'request': request})
        self.response['data'] = serializer.data
        self.response['status'] = status.HTTP_200_OK
        self.response['message'] = 'Successfully Get All The Album'
        return Response(self.response, status=self.response['status'])


class GetAlbumsTracks(APIView):
    """
    Get Albums Tracks
    """
    def __init__(self):
        self.response = ResponseInfo().response

    def get_track(self, album_id):
        try:
            album = Album.objects.get(id=album_id)
            track_obj = Track.objects.filter(album_name=album)
            return track_obj
        except Album.DoesNotExist:
            return False

    @swagger_auto_schema(
        operation_description="This API used for get a all tracks for a particular album"
    )
    def get(self, request, album_id):
        track_obj = self.get_track(album_id)
        if track_obj:
            try:
                paginator = CustomPaginator()
                page = paginator.paginate_queryset(track_obj, request)
                serializer = AlbumsTrackSerializer(page, many=True)
                result = paginator.get_paginated_response(serializer.data, album_id)
                self.response['data'] = result.data
                self.response['message'] = 'Successfully Get the Album'
            except Exception as e:
                self.response['message'] = 'Something went wrong'
                self.response['status'] = status.HTTP_400_BAD_REQUEST
        else:
            self.response['message'] = 'No Album Found with this id'
            self.response['status'] = status.HTTP_400_BAD_REQUEST
        return Response(self.response, status=self.response['status'])


class GetAllNewReleasesAlbum(APIView):
    """
    Get all New Realease Albums
    """
    def __init__(self):
        self.response = ResponseInfo().response

    def get_albums(self):
        try:
            thirty_days_threshold = datetime.now(pytz.timezone('Asia/Kolkata')) - timedelta(days=30)
            obj = Album.objects.filter(release_date__gt=thirty_days_threshold, active=True)
            return obj
        except Album.DoesNotExist:
            return False

    @swagger_auto_schema(
        operation_description="This API used for get a all new album"
    )
    def get(self, request):
        albums = self.get_albums()
        serializer = AlbumSerializer(albums, many=True, context={'request': request})
        self.response['data'] = serializer.data
        self.response['status'] = status.HTTP_200_OK
        self.response['message'] = 'Successfully Get All The Album'
        return Response(self.response, status=self.response['status'])