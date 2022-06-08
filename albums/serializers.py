from rest_framework import serializers
from .models import Album, Artist, Track, AlbumsImage, ArtistsImage
from .utils import CustomPaginator


class ArtistImageSerializer(serializers.ModelSerializer):
    """
    Serializer for ArtistsImage model
    """
    class Meta:
        model = ArtistsImage
        fields = "__all__"


class ArtistSerializer(serializers.ModelSerializer):
    """
    Serializer for Artist model
    """
    artist_image = serializers.SerializerMethodField()
    class Meta:
        model = Artist
        fields = ['id','artist_name','short_bio','popularity','external_urls','artist_image']

    def get_artist_image(self, obj):
        obj = ArtistImageSerializer(ArtistsImage.objects.filter(artist_name=obj), many=True)
        return obj.data


class TrackSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Track model
    """
    class Meta:
        model = Track
        fields = ['id' , 'track_name', 'url']


class AlbumsImageSerializer(serializers.ModelSerializer):
    """
    Serializer for AlbumsImage model
    """
    class Meta:
        model = AlbumsImage
        fields = "__all__"


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Album model
    """
    available_markets = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    tracks = serializers.SerializerMethodField('paginated_tracks')
    artists = ArtistSerializer(source='artist', many=True)

    class Meta:
        model = Album
        fields = ['id','name','type','total_tracks','release_date','release_date_precision','uri','active','created_at','available_markets','updated_at','artists','tracks', 'images']

    def get_available_markets(self, obj):
        return obj.available_markets

    def paginated_tracks(self, obj=None):
        tracks = Track.objects.filter(album_name=obj)
        paginator = CustomPaginator()
        page = paginator.paginate_queryset(tracks, self.context['request'])
        serializer = TrackSerializer(page, many=True, context={'request': self.context['request']})
        result = paginator.get_paginated_response(serializer.data, obj.id)
        return result.data

    def get_images(self, obj):
        obj = AlbumsImageSerializer(AlbumsImage.objects.filter(album_name=Album.objects.get(id=obj.id)), many=True)
        return obj.data


class AlbumsTrackSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Track model
    """
    class Meta:
        model = Track
        fields = ['id' , 'track_name', 'url']