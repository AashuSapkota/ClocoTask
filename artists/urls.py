from .import views
from django.urls import path

app_name = 'artists'

urlpatterns = [

    # url for artists
    path('register/', views.RegisterArtistAPI.as_view(), name='register_artist'),
    path('list/', views.ListArtistsAPI.as_view(), name='list_artist'),
    path('update/<int:artist_id>', views.UpdateArtistAPI.as_view(), name='update_artist'),
    path('delete/<int:artist_id>', views.DeleteArtistAPI.as_view(), name='delete_artist'),
    path('fetch/similar/', views.FetchSimilarArtist.as_view(), name='similar_atrist'),

    # url for music
    path('music/register/', views.RegisterMusicAPI.as_view(), name='register_artist_music'),
    path('music/list/', views.ListArtistMusicAPI.as_view(), name='list_artist_music'),
]