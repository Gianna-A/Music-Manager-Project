# Write your models here
from django.db import models
from django.template.defaultfilters import slugify
from .validators import dateValidator
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


Formats = (("DD", "Digital Download"), ("CD", "CD"),("VL", "Vinyl"))
UserTypes =(("Artist", "Artist"), ("Editor", "Editor"), ("Viewer", "Viewer"))


class Song(models.Model):
    title = models.CharField(null = False, blank = False, max_length = 512)
    runtime = models.IntegerField(validators=[MinValueValidator(10)], null=False, blank=False)
    
    def __str__(self):
        return self.title
    
class Album(models.Model):
    title = models.CharField(max_length = 512, null = False, blank = False)
    description = models.TextField(blank = True, null = False, default="")
    artist = models.CharField(max_length=512, null=False, blank=False)
    cover_image = models.ImageField(blank = True, null = True, default="no_cover.jpg", upload_to="")
    price = models.DecimalField(max_digits=5, decimal_places=2, blank = False, null = False, validators=[MinValueValidator(Decimal(0)), MaxValueValidator(Decimal(999.99))])
    format = models.CharField(choices=Formats, max_length=512)
    release_date = models.DateField(validators=[dateValidator], blank = True, null = True)
    tracks = models.ManyToManyField(Song, through="AlbumTrackListItem", related_name='albums')
    
    class Meta:
        unique_together = ["title", "artist", "format"]
    
    slug = models.SlugField(null=True, editable=False)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.cover_image:
            self.cover_image = "no_cover.jpg"
        if not self.slug:
            self.slug = slugify(self.title)
        #super().save(*args, **kwargs)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class AlbumTrackListItem(models.Model):
    position = models.IntegerField(validators=[MinValueValidator(1)], blank = True, null=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    class Meta:
        unique_together = ['album', 'song']
        ordering = ['album', 'position']
        
    
class MusicManagerUser(models.Model):
    display_name = models.CharField(max_length=512)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    class Meta:
        permissions = [
            ("artist", "Can view and change only their own album"),
            ("editor", "Can view, change, add, and delete all albums"),
            ("viewer", "can view albums"),
        ]    
    
        