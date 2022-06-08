from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Track)
admin.site.register(AlbumsImage)
admin.site.register(ArtistsImage)