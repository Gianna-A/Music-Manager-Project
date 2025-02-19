# Write your tests here. Use only the Django testing framework.
from django.test import TestCase
from .models import Album, Song, MusicManagerUser, AlbumTrackListItem
from .forms import AlbumForm
from datetime import date
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Permission
from django.urls import reverse
from rest_framework import status
from django.contrib.messages import get_messages

#test models
class AlbumSongATLITest(TestCase):
    def testData(self):
        album = Album.objects.create(title="Flowers", description="Many Flowers Bloom all Day", artist="Rose", price=35.00, format="DD", release_date=date(2023, 6, 6))
        song = Song.objects.create(title="Lily in May", runtime=200)
        song2 = Song.objects.create(title="Poppies in November", runtime=200)
        album.tracks.add(song, song2)
        
        album = Album.objects.get(pk=1)
        # title
        self.assertEqual(album.title, "Flowers")
        # description
        self.assertEqual(album.description, "Many Flowers Bloom all Day")
        # artist
        self.assertEqual(album.artist, "Rose")
        # price
        self.assertEqual(album.price, 35.00)
        # format
        self.assertEqual(album.format, "DD")
        # release date
        self.assertEqual(album.release_date, date(2023, 6, 6))
        # tracks
        self.assertEqual(album.tracks.count(), 2)
        self.assertEqual(album.tracks.first().title, "Lily in May")
        self.assertEqual(album.tracks.get(pk=2).title, "Poppies in November")
        # cover image
        self.assertEqual(album.cover_image, "no_cover.jpg")
        # slug
        self.assertEqual(album.slug, "flowers")       
    
    def testValidation(self):
        with self.assertRaises(ValidationError):
            album = Album.objects.create(title="Flowers", description="Many Flowers Bloom all Day", artist="Rose", price=1000, format="DD", release_date=date(2023, 6, 6))
        
        with self.assertRaises(ValidationError):
            album = Album.objects.create(title="Flowers", description="Many Flowers Bloom all Day", artist="Rose", price=25.00, format="DD", release_date=date(2028, 6, 6))


class MusicManagerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="KSmith", password = "smith8")
        self.music_manager_user = MusicManagerUser.objects.create(user=self.user, display_name="Karen Smith")
    def testingUser(self):
        first_user = MusicManagerUser.objects.get(user=self.user)
        self.assertEqual(first_user.user.username, "KSmith")
        self.assertEqual(first_user.display_name, "Karen Smith")
        
    def testPermissions(self):
        permisson = Permission.objects.get(codename="artist")
        self.user.user_permissions.add(permisson)
        self.assertTrue(self.user.has_perm("label_music_manager.artist"))
        self.assertFalse(self.user.has_perm("label_music_manager.editor"))
        
        
#test forms
class testAlbumForm(TestCase):
    def newAlbum(self):
        form = AlbumForm()
        fields = ['title', 'description', 'artist', 'cover_image', 'price', 'format', 'release_date', 'tracks']
        for field in fields:
            self.assertIn(field, form.fields)

#test views
#api
class AlbumTrackViewTest(TestCase):
    def setUp(self):
        self.album1= Album.objects.create(title="Flowers", description="Many Flowers Bloom all Day", artist="Rose", price=80.00, format="DD", release_date=date(2023, 6, 6))
        self.album2 = Album.objects.create(title="Daisy", description="Walking in the grass", artist="Mary Poppins",price=15.00,format="CD", release_date=date(2023,5,1))
        self.song1 = Song.objects.create(title="Lily in May", runtime=200)
        self.song2 = Song.objects.create(title="Poppies in November", runtime=230)
        self.song3 = Song.objects.create(title="Daisy World", runtime=245)
        self.song4 = Song.objects.create(title="Grass Meadow", runtime=183)
        self.album1.tracks.add(self.song1, self.song2)
        self.album2.tracks.add(self.song3, self.song4)
        
    def test_all_Albums(self):
        response = self.client.get(reverse('album-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Flowers")
        self.assertContains(response, "Daisy")
    def test_detail_view(self):
        response = self.client.get(reverse('album-detail', args=[self.album1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Flowers")
        self.assertContains(response, 430)
        self.assertContains(response, "Lily in May")
        self.assertContains(response, "Poppies in November")
        self.assertNotContains(response, "Daisy")
        self.assertNotContains(response, "Daisy World")
        self.assertNotContains(response, "Grass Meadow")
        
    def testTrackList_View(self):
        response = self.client.get(reverse('track-detail', kwargs={'track_id': 1}))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['album'], self.album1.id)
        self.assertEqual(response_data['song'], self.song1.id)
    
    def testCreateAlbum(self):
        data = {'title': 'Aliens on the Beach', 'description': 'Who may be wandering around you?', 'artist': 'The Amazing Alien', 'price': 35.00, 'format': 'DD', 'release_date': date(2023, 8, 9)}
        response12 = self.client.post(reverse('album-list'), data)
        self.assertEqual(response12.status_code, 201)

    def testPartialUpdate(self):
        data = {'description' : "Many have known before"}
        response9 = self.client.patch(reverse('album-detail', args=[self.album2.id]), data,  content_type='application/json')
        self.assertEqual(response9.status_code, 200)
    def testfull_update(self):
        data = {'title': 'Updated Title','description': 'Updated description','artist': 'Updated Artist','price': 35.00,'format': 'DD','release_date': '2023-06-06'}
        response9 = self.client.put(reverse('album-detail', args=[self.album2.id]), data,  content_type='application/json')
        self.assertEqual(response9.status_code, 200)
    def testDeleteAlbum(self):
        response9 = self.client.delete(reverse('album-detail', args=[self.album1.id]))
        self.assertEqual(response9.status_code, 204)
    
class SongListViewTest(TestCase):
    def setUp(self):
        self.song1 = Song.objects.create(title="Lily in May", runtime=200)
        self.song2 = Song.objects.create(title="Poppies in November", runtime=230)
        self.song3 = Song.objects.create(title="Daisy World", runtime=245)
        self.song4 = Song.objects.create(title="Grass Meadow", runtime=183)
    def test_all_Songs(self):
        response = self.client.get(reverse('song-list'))
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lily in May")
        self.assertContains(response, "Daisy World")
        self.assertContains(response, self.song1.title)
        self.assertContains(response, self.song1.runtime)
    def test_detail_view(self):
        response = self.client.get(reverse('song-detail', args=[self.song1.id]))
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.song1.title)
        self.assertContains(response, self.song1.runtime)
        self.assertNotContains(response, "Daisy World")
        self.assertEqual(response.status_code, 200) 
    def testcreateSongs(self):
        data = {'title': 'My name', 'runtime': 200}
        response14 = self.client.post(reverse('song-list'), data)
        self.assertEqual(response14.status_code, 201)
    def testPartialUpdate(self):
        data = {'runtime' : 100}
        
        response9 = self.client.patch(reverse('song-detail', args=[self.song2.id]), data,  content_type='application/json')
        self.assertEqual(response9.status_code, 200) 
    def testdeleteSongs(self):
        response9 = self.client.delete(reverse('song-detail', args=[self.song1.id]))
        self.assertEqual(response9.status_code, 204)

#templated
class testingTemplatedViews(TestCase):
    def setUp(self):
        #adding/creating an artist user
        self.userArtist = User.objects.create_user(username="KSmith", password = "smith8")
        self.music_manager_user = MusicManagerUser.objects.create(user=self.userArtist, display_name="Rose")
        permisson = Permission.objects.get(codename="artist")
        
        #adding/creating an editor user
        self.userEditor = User.objects.create_user(username="editor9", password = "smith8")
        self.music_manager_user = MusicManagerUser.objects.create(user=self.userEditor, display_name="Jim Bow")
        permisson1 = Permission.objects.get(codename="editor")
        
        #adding/creating a viewer user
        self.userViewer = User.objects.create_user(username="viewer9", password = "smith8")
        self.music_manager_user = MusicManagerUser.objects.create(user=self.userViewer, display_name="Ray Zin")
        permisson2 = Permission.objects.get(codename="viewer")
        
        self.userArtist.user_permissions.add(permisson)
        self.userEditor.user_permissions.add(permisson1)
        self.userViewer.user_permissions.add(permisson2)
        
        #setting up albums and songs
        self.album1= Album.objects.create(title="Flowers", description="Many Flowers Bloom all Day", artist="Rose", price=80.00, format="DD", release_date=date(2023, 6, 6))
        self.album2 = Album.objects.create(title="Daisy", description="Walking in the grass", artist="Mary Poppins",price=15.00,format="CD", release_date=date(2023,5,1))
        self.song1 = Song.objects.create(title="Lily in May", runtime=200)
        self.song2 = Song.objects.create(title="Poppies in November", runtime=230)
        self.song3 = Song.objects.create(title="Daisy World", runtime=245)
        self.song4 = Song.objects.create(title="Grass Meadow", runtime=183)
        self.album1.tracks.add(self.song1, self.song2)
        self.album2.tracks.add(self.song3, self.song4)
    
    def test_Login(self):
        self.client.login(username="KSmith", password = "smith8")
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertTemplateNotUsed(response, 'label_music_manager/create_album.html')
    
    def test_Artist_Routes(self):
        #artist view album list
        self.client.login(username="KSmith", password = "smith8")
        response = self.client.get(reverse('list-album'))  
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Flowers")
        self.assertNotContains(response, "Daisy")
        self.assertNotContains(response, "Add Album")
        
        #raise a Forbidden error for new album | artist
        response2 = self.client.get(reverse('create-album'))
        self.assertEqual(response2.status_code, 403)
        
        #artist Detail view
        response3 = self.client.get(reverse('detail-view', args=[self.album1.id]))
        self.assertEqual(response3.status_code, 200)
        self.assertTemplateUsed(response3, 'label_music_manager/album_detail_view.html')
        self.assertContains(response3, "Flowers")
        self.assertNotContains(response3, "Daisy")
        self.assertContains(response3, "Edit Album")
        self.assertContains(response3, "Delete Album")
        
        #artist edit album
        response4 = self.client.get(reverse('edit-album', kwargs={'album_id': self.album1.id}))
        self.assertEqual(response4.status_code, 200)
        self.assertTemplateUsed(response4, 'label_music_manager/update_album.html')
        self.assertContains(response4, '<form')
        
        #post form request
        data = {'title': 'Flowers', 'description': 'A new description for the Flowers album','artist': 'Rose','price': 35.00,'format': 'DD','release_date': date(2023,6,6)}
        url = reverse('edit-album',  kwargs={'album_id': self.album1.id})
        response9 = self.client.post(url, data)
        self.assertEqual(response9.status_code, 302)
        messages = [msg.message for msg in get_messages(response9.wsgi_request)]
        self.assertIn('Album successfully Updated', messages)
        
        #raise a Forbidden error editing another album
        response5 = self.client.get(reverse('edit-album', args=[self.album2.id]))
        self.assertEqual(response5.status_code, 403)
        
        #check the delete view
        response6 = self.client.get(reverse('delete-view', args=[self.album1.id]))
        self.assertEqual(response6.status_code, 200)
        
        #check delete POST request forbidden
        response7 = self.client.post(reverse('delete-view', kwargs={'album_id': self.album1.id}))
        self.assertEqual(response7.status_code, 403)
        
        #check delete view forbidden with different album
        response8 = self.client.get(reverse('delete-view', args=[self.album2.id]))
        self.assertEqual(response8.status_code, 403)
        
        #check slug
        response10 = self.client.get(reverse('detail-view', kwargs={'slug': self.album1.slug, 'album_id': self.album1.id}))
        self.assertEqual(response10.status_code, 200)
                                
    
    def test_Viewer_Routes(self):
        self.client.logout()
        self.client.login(username="viewer9", password = "smith8")
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertTemplateNotUsed(response, 'label_music_manager/create_album.html')
        
        #viewer album list
        response1 = self.client.get(reverse('list-album'))  
        self.assertEqual(response1.status_code, 200)
        self.assertContains(response1, "Flowers")
        self.assertContains(response1, "Daisy")
        self.assertNotContains(response1, "Add Album")
        
        #raise a Forbidden error for new album | viewer
        response2= self.client.get(reverse('create-album'))
        self.assertEqual(response2.status_code, 403)
        
        #viewer Detail view
        response3 = self.client.get(reverse('detail-view', args=[self.album1.id]))
        self.assertEqual(response3.status_code, 200)
        self.assertTemplateUsed(response3, 'label_music_manager/album_detail_view.html')
        self.assertContains(response3, "Flowers")
        self.assertNotContains(response3, "Daisy")
        self.assertNotContains(response3, "Edit Album")
        self.assertNotContains(response3, "Delete Album")
        
        #artist edit album forbidden
        response4 = self.client.get(reverse('edit-album', args=[self.album1.id]))
        self.assertEqual(response4.status_code, 403)
        
        #check the delete view forbidden
        response6 = self.client.get(reverse('delete-view', args=[self.album1.id]))
        self.assertEqual(response6.status_code, 403)
        
        
        #check slug
        response10 = self.client.get(reverse('detail-view', kwargs={'slug': self.album2.slug, 'album_id': self.album2.id}))
        self.assertEqual(response10.status_code, 200)
                                
    def test_Editor_Routes(self):
        self.client.logout()
        self.client.login(username="editor9", password = "smith8")
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertTemplateNotUsed(response, 'label_music_manager/create_album.html')
        
        # new album get | editor
        response2 = self.client.get(reverse('create-album'))
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, '<form')
        
        #editor album list
        response1 = self.client.get(reverse('list-album'))  
        self.assertEqual(response1.status_code, 200)
        self.assertContains(response1, "Flowers")
        self.assertContains(response1, "Daisy")
        self.assertContains(response1, "Add Album")
        
        #new album post | editor
        data2 = {'title': 'Aliens on earth','description': 'Who may be wandering around you?','artist': 'The Amazing Alien','price': 35.00,'format': 'DD', 'release_date': date(2023,8,9)}
        response11 = self.client.post(reverse('create-album'), data2)
        self.assertEqual(response11.status_code, 302)  
        messages1 = [msg.message for msg in get_messages(response11.wsgi_request)]
        self.assertIn('Album successfully Created', messages1)
        
        #editor Detail view
        response3 = self.client.get(reverse('detail-view', args=[self.album1.id]))
        self.assertEqual(response3.status_code, 200)
        self.assertTemplateUsed(response3, 'label_music_manager/album_detail_view.html')
        self.assertContains(response3, "Flowers")
        self.assertNotContains(response3, "Daisy")
        self.assertContains(response3, "Edit Album")
        self.assertContains(response3, "Delete Album")
        
        #edit edit album
        response4 = self.client.get(reverse('edit-album', args=[self.album1.pk]))
        self.assertEqual(response4.status_code, 200)
        self.assertTemplateUsed(response4, 'label_music_manager/update_album.html')
        self.assertContains(response, '<form')
        
        #post form request
        data2 = {'title': 'Flowers','description': 'A new description for the Flowers album','artist': 'Rose','price': 35.00,'format': 'DD','release_date': date(2023, 6, 6)}
        url =  url = reverse('edit-album', kwargs={'album_id': self.album1.id})
        self.assertIsNotNone(self.album1.id)
        response15 = self.client.post(url, data2)
        self.assertEqual(response15.status_code, 302)
        messages = [msg.message for msg in get_messages(response15.wsgi_request)]
        self.assertIn('Album successfully Updated', messages)
        
        #check the delete view
        response6 = self.client.get(reverse('delete-view', args=[self.album1.id]))
        self.assertEqual(response6.status_code, 200)
        
        #check delete POST request
        response7 = self.client.post(reverse('delete-view', kwargs={'album_id': self.album2.id}))
        self.assertEqual(response7.status_code, 302)
        
        #check slug
        response10 = self.client.get(reverse('detail-view', kwargs={'slug': self.album1.slug, 'album_id': self.album1.id}))
        self.assertEqual(response10.status_code, 200)
                                