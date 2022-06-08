from email.policy import default
from django.db import models
from django.forms import JSONField
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .utils import delete_file

class Artist(models.Model):
    """
    Artist model
    """
    artist_name = models.CharField(max_length=100, null=False, blank=False)
    short_bio = models.CharField(max_length=255, null=True, blank=True)
    popularity = models.BigIntegerField(default=0)
    external_urls = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.artist_name



class Album(models.Model):
    """
    Album Model
    """
    name = models.CharField(max_length=150, null=False, blank=False)
    type = models.CharField(max_length=55, default='album')
    total_tracks = models.BigIntegerField(default=0)
    release_date = models.DateField(null=True, blank=True)
    release_date_precision = models.CharField(max_length=150, null=True, blank=True)
    uri = models.CharField(max_length=150, null=True, blank=True)
    artist = models.ManyToManyField(Artist)
    available_markets = models.JSONField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Track(models.Model):
    """
    Track Model
    """
    track_name = models.CharField(max_length=200, null=False, blank=False)
    url        = models.FileField(upload_to='track/')
    album_name = models.ForeignKey(Album, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.track_name

@receiver(post_save,sender=Track)
def create_track(sender,instance,created,**kwargs):
    instance.album_name.total_tracks = instance.album_name.total_tracks + 1
    instance.album_name.save()
        
@receiver(post_delete,sender=Track)
def delete_track(sender,instance,*args,**kwargs):
    instance.album_name.total_tracks = instance.album_name.total_tracks - 1
    instance.album_name.save()

    if instance.url:
        delete_file(instance.url.path)


class AlbumsImage(models.Model):
    """
    Albums Image Model
    """
    image_url = models.FileField(upload_to='albums_image/')
    album_name = models.ForeignKey(Album, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.album_name.name

@receiver(post_delete,sender=AlbumsImage)
def delete_albums_image(sender,instance,*args,**kwargs):
    if instance.image_url:
        delete_file(instance.image_url.path)



class ArtistsImage(models.Model):
    """
    Artists Image model
    """
    image_url = models.FileField(upload_to='artist_image/')
    artist_name = models.ForeignKey(Artist, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.artist_name.artist_name

@receiver(post_delete,sender=ArtistsImage)
def delete_artist_image(sender,instance,*args,**kwargs):
    if instance.image_url:
        delete_file(instance.image_url.path)