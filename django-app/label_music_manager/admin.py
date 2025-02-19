from django.contrib import admin
from .models import Song, Album, AlbumTrackListItem, MusicManagerUser
from django.contrib.auth.models import Group, Permission
from django.apps import apps


admin.site.register(Song)
admin.site.register(Album)
admin.site.register(AlbumTrackListItem)
admin.site.register(MusicManagerUser)