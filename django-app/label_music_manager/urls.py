# Use this file to specify your subapp's routes
from django.urls import path
from label_music_manager.api_views import AlbumViewSet, SongsViewSet, ATLIViewSet, apiRootViewSet
from label_music_manager.views import ListAlbumView, LoginAccountView, LogoutAccountView, DetailAlbumView, SlugAlbumView,  DeleteAlbumView, NewAlbumView, EditAlbumView

albums_list_view = AlbumViewSet.as_view({'get': 'list', 'post': 'create'})
albums_detail_view = AlbumViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'patch': 'partial_update', 'put': 'full_update'})
songs_list_view = SongsViewSet.as_view({'get': 'list', 'post': 'create'})
songs_detail_view = SongsViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'patch': 'partial_update', 'put': 'full_update'})
track_list_view = ATLIViewSet.as_view({'get': 'list', 'post': 'create'})
track_detail_view = ATLIViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'patch': 'partial_update', 'put': 'full_update'})
api_list_view = apiRootViewSet.as_view({'get': 'list'})

urlpatterns = [
    #api routes
    path('api/albums/', albums_list_view, name ='album-list'),
    path('api/albums/<int:album_id>/', albums_detail_view, name='album-detail'),
    path('api/', api_list_view ),
    path('api/songs/', songs_list_view, name='song-list'),
    path('api/songs/<int:song_id>/', songs_detail_view, name='song-detail'),
    path('api/tracklist/', track_list_view, name='track-list'),
    path('api/tracklist/<int:track_id>/', track_detail_view, name='track-detail'),
    #templated routes
    path('accounts/login/', LoginAccountView.as_view(), name = 'login'),
    path('accounts/logout/', LogoutAccountView.as_view(), name = 'logout'),
    path('albums/<int:album_id>/', DetailAlbumView.as_view(), name = 'detail-view'),
    path('albums/<int:album_id>/delete/',  DeleteAlbumView.as_view(), name = 'delete-view'),
    path('albums/<int:album_id>/edit/', EditAlbumView.as_view(), name='edit-album'),
    path('albums/<int:album_id>/<slug:slug>/', SlugAlbumView.as_view(), name='detail-view'),
    path('albums/new/', NewAlbumView.as_view(), name='create-album'),
    path('', ListAlbumView.as_view(), name = 'list-album'),
]
