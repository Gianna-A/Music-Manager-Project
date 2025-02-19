# Use this file for your API viewsets only
# E.g., from rest_framework import ...
from rest_framework import viewsets
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Song, Album, AlbumTrackListItem, MusicManagerUser
from .serializers import SongSerializer, AlbumSerializer, ATLISerializer, MusicManagerSerializer

# Create your views here.

class AlbumViewSet(viewsets.ViewSet):
    
    def list(self, request):
        queryset = Album.objects.all()
        serializer = AlbumSerializer(queryset, many = True, context={'request': request})
        
        return Response(serializer.data)
    
    def create(self, request):
        serializer = AlbumSerializer(data = request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def retrieve(self, request, album_id=None):
        queryset = Album.objects.all()
        album = get_object_or_404(queryset, pk=album_id)
        serializer = AlbumSerializer(album, context={'request': request})
        return Response(serializer.data)
    
    def destroy(self, request, album_id=None):
        try:
            album = Album.objects.get(pk = album_id)
            album.delete()
            return Response({"message": "Successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        except:
            raise NotFound(detail="Album not found")
        
    def partial_update(self, request, album_id=None):
        try:
            album = Album.objects.get(pk=album_id)
        except Album.DoesNotExist:
            return Response({"detail": "Album not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AlbumSerializer(album, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def full_update(self, request, album_id=None):
        try:
            album = Album.objects.get(pk=album_id)
        except Album.DoesNotExist:
            return Response({"detail": "Album not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AlbumSerializer(album, data=request.data, partial=False, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SongsViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Song.objects.all()
        serializer = SongSerializer(queryset, many = True, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):
        serializer = SongSerializer(data = request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def retrieve(self, request, song_id=None):
        queryset = Song.objects.all()
        song = get_object_or_404(queryset, pk=song_id)
        serializer = SongSerializer(song, context={'request': request})
        return Response(serializer.data)
    
    def destroy(self, request, song_id=None):
        try:
            song = Song.objects.get(pk = song_id)
            song.delete()
            return Response({"message": "Successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        except:
            raise NotFound(detail="Song not found")
        
    def partial_update(self, request, song_id=None):
        try:
            song = Song.objects.get(pk=song_id)
        except Song.DoesNotExist:
            return Response({"detail": "Song not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = SongSerializer(song, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def full_update(self, request, song_id=None):
        try:
            song = Song.objects.get(pk=song_id)
        except Song.DoesNotExist:
            return Response({"detail": "Song not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = SongSerializer(song, data=request.data, partial=False, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ATLIViewSet(viewsets.ViewSet):
    
    def list(self, request):
        queryset = AlbumTrackListItem.objects.all()
        serializer = ATLISerializer(queryset, many = True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = ATLISerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def retrieve(self, request, track_id=None):
        queryset = AlbumTrackListItem.objects.all()
        tracklist = get_object_or_404(queryset, pk=track_id)
        serializer = ATLISerializer(tracklist)
        return Response(serializer.data)
    
    def destroy(self, request, track_id=None):
        try:
            tracklist = AlbumTrackListItem.objects.get(pk = track_id)
            tracklist.delete()
            return Response({"message": "Successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        except:
            raise NotFound(detail="tracklist not found")
        
    def partial_update(self, request, track_id=None):
        try:
            tracklist = AlbumTrackListItem.objects.get(pk=track_id)
        except AlbumTrackListItem.DoesNotExist:
            return Response({"detail": "tracklist not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ATLISerializer(tracklist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def full_update(self, request, track_id=None):
        try:
            tracklist = AlbumTrackListItem.objects.get(pk=track_id)
        except AlbumTrackListItem.DoesNotExist:
            return Response({"detail": "tracklist not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ATLISerializer(tracklist, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class apiRootViewSet(viewsets.ViewSet):
    
    def list(self, request):
        base_url = request.build_absolute_uri('/').rstrip('/')
        representation = {
            'albums' : base_url + reverse('album-list'),
            'songs' : base_url + reverse('song-list'),
            'tracklist': base_url + reverse('track-list'),
        }
        return Response(representation)