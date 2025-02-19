# Use this file for your templated views only
from django.views import View
from django.views.generic import DetailView
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from .models import Album, Song, AlbumTrackListItem, MusicManagerUser
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import AlbumForm
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin

#no 1
class ListAlbumView(View):
    
    def get(self, request):
        context = {}
        if request.user.is_authenticated:
           #get display name
            user_profile =  get_object_or_404(MusicManagerUser, user=request.user)
            #if user is artist, print the artist's albums only by linking display_name with album model artist
            if request.user.has_perm('label_music_manager.artist'):
                album = Album.objects.filter(artist=user_profile.display_name)
                context["album_list"] = album
            else:
                album = Album.objects.all()
            for a in album:
                if len(a.description) > 255:
                    a.description = a.description[:255] + "..."
                if a.format == "VL":
                    a.format = "Vinyl"
                elif a.format == "DD":
                    a.format = "Digital Download"
            
            context["album_list"] = album
            context["displayName"] = user_profile.display_name
            context["username"] = request.user.username
        else:
            album_list = Album.objects.all()
            for album in album_list:
                if len(album.description) > 255:
                    album.description = album.description[:255] + "..."
            context["album_list"] = album_list
            context["displayName"] = 'Guest'
            context["username"] = ''
        context['isEditor'] = request.user.has_perm('label_music_manager.editor')
        return render(request, "label_music_manager/album_list_views.html", context)
    
class DetailAlbumView(View):
    
    #no 3
    def get(self, request, album_id=None):
        context = {}
        if request.user.is_authenticated:
             user_profile =  get_object_or_404(MusicManagerUser, user=request.user)
             context["displayName"] = user_profile.display_name
             context["username"] = request.user.username
        queryset = Album.objects.all()
        album = get_object_or_404(queryset, pk = album_id)
        if album.format == "VL":
            album.format = "Vinyl"
        elif album.format == "DD":
            album.format = "Digital Download"
        context['album_detail'] = album
        context['can_delete'] = request.user.has_perm('label_music_manager.editor') or request.user.has_perm('label_music_manager.artist')
        #getting the tracklist
        tracks = AlbumTrackListItem.objects.filter(album = album_id)
        context['tracklist'] = tracks
        return render(request, "label_music_manager/album_detail_view.html", context)
    #no 5

class SlugAlbumView(View):
    
    #no 4
    def get (self, request, album_id=None, slug=None):
        context = {}
        user_profile =  get_object_or_404(MusicManagerUser, user=request.user)
        queryset = Album.objects.all()
        album = get_object_or_404(queryset, pk = album_id, slug=slug)
        if album.format == "VL":
            album.format = "Vinyl"
        elif album.format == "DD":
            album.format = "Digital Download"
        context['can_delete'] = request.user.has_perm('label_music_manager.editor') and request.user.has_perm('label_music_manager.artist')
        context['album_detail'] = album
        context["displayName"] = user_profile.display_name
        context["username"] = request.user.username
        return render(request, "label_music_manager/album_detail_view.html", context)
    
class NewAlbumView(PermissionRequiredMixin, View):
    permission_required = 'label_music_manager.editor'
    raise_exception = True
    #no 6a
    def get(self, request):
        context = {}
        user_profile =  get_object_or_404(MusicManagerUser, user=request.user)
        context["displayName"] = user_profile.display_name
        context["username"] = request.user.username
        context["form"] = AlbumForm()
        return render(request, 'label_music_manager/create_album.html', context)
    #no 2
    def post(self, request):
        context = {}
        form = AlbumForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Album successfully Created")
            return HttpResponseRedirect(reverse('list-album'))

class EditAlbumView(View):
    
    #no 6b
    def get(self, request, album_id):
        context = {}
        
        user_profile =  get_object_or_404(MusicManagerUser, user=request.user)
        album = get_object_or_404(Album, pk=album_id)
        if user_profile.display_name == album.artist or request.user.has_perm('label_music_manager.editor'):
            form = AlbumForm(request.POST or None, instance = album)
            context["form"] = form
            context["album"] = album
            context["displayName"] = user_profile.display_name
            context["username"] = request.user.username
            return render(request, 'label_music_manager/update_album.html', context)

        else:
            return HttpResponseForbidden("You do not have permission to delete this album.")
    def post(self, request, album_id):
        album = get_object_or_404(Album, pk=album_id)
        form = AlbumForm(request.POST or None, instance = album)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Album successfully Updated")
            return HttpResponseRedirect(reverse('list-album'))
        else:
            return render(request, 'label_music_manager/update_album.html', {'form': form})


class DeleteAlbumView(View):
    
    #no 7
    def get(self, request, album_id):
        context ={}
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You do not have permission to delete this album.")
        
        
        #displayname
        user_profile =  get_object_or_404(MusicManagerUser, user=request.user)
        context["displayName"] = user_profile.display_name
        context["username"] = request.user.username
        album = get_object_or_404(Album, pk=album_id)
        
        if user_profile.display_name == album.artist or request.user.has_perm('label_music_manager.editor'):
            context['album_detail'] = album
            return render(request, "label_music_manager/delete_view.html", context)
        else:
            return HttpResponseForbidden("You do not have permission to delete this album.")
    
    #no 8
    def post(self, request, album_id):
        if not request.user.has_perm('label_music_manager.editor'):
            return HttpResponseForbidden("You do not have permission to delete this album.")
        else:
            album = get_object_or_404(Album, pk = album_id)
            album.delete()
            messages.add_message(request, messages.SUCCESS, "Album successfully deleted")
            return HttpResponseRedirect(reverse('list-album'))
    
class LoginAccountView(View):
    
    #no 9
    def get(self, request):
        return render(request, 'login.html')
    #no 10
    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('list-album'))
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

class LogoutAccountView(View):
    
    #no 11
    def post(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('list-album'))