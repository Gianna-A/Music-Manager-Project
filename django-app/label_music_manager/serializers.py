# Write your serialisers here
from rest_framework import serializers
from django.urls import reverse
from .models import Song, Album, AlbumTrackListItem, MusicManagerUser

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'
    
    def to_representation(self, instance):
        
        request = self.context.get('request')
        base_url = request.build_absolute_uri('/').rstrip('/') if request else 'http://127.0.0.1:8000'
        
        representation = {
            'id' : instance.id,
            'url' : f"{base_url}{reverse('song-list')}{instance.id}/",
            'title': instance.title,
            'length': instance.runtime
        }
        return representation

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'
        
    def to_representation(self, instance):
        
        request = self.context.get('request')
        base_url = request.build_absolute_uri('/').rstrip('/') if request else 'http://127.0.0.1:8000'
        
        sum_tp = 0
        for track in instance.tracks.all():
            sum_tp += track.runtime
        
        #check description is greater than 255 then put ellipses
        def check_length():
            if (len(instance.description) > 255):
                return instance.description[:255] + "..."
            else:
                return instance.description
        representation = {
            'id' : instance.id,
            'total_playtime' : sum_tp,
            'description_short': check_length(), #shortened
            'release_year': instance.release_date.year,
            'tracks': SongSerializer(instance.tracks.all(), many=True, context={'request': request}).data,
            'url': f"{base_url}{reverse('album-list')}{instance.id}/",
            'cover_image': f"{base_url}/media/{instance.cover_image}",
            'title': instance.title,
            'description': instance.description,
            'artist': instance.artist,
            'price': f"{instance.price:.2f}",
            'format': instance.format,
            'release_date': instance.release_date,
            'slug': instance.slug,
        }
        return representation
        
class ATLISerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumTrackListItem
        fields = '__all__'

class MusicManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicManagerUser
        fields = '__all__'