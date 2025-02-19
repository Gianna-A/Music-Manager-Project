# If you require forms, write them here
from django import forms
from .models import Album, AlbumTrackListItem, Song

class AlbumForm(forms.ModelForm):
    
    tracks = forms.ModelMultipleChoiceField(queryset=Song.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    release_date = forms.DateField(widget = forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Album
        fields = ['title', 'description', 'artist', 'cover_image', 'price', 'format', 'release_date', 'tracks']

