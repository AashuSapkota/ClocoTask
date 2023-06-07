from .import views
from django.urls import path

app_name = 'artists'

urlpatterns = [
    path('register/', views.RegisterArtistAPI.as_view(), name='register_artist'),
    path('list/', views.ListArtistsAPI.as_view(), name='list_artist'),
    path('update/<int:artist_id>', views.UpdateArtistAPI.as_view(), name='update_artist'),
    path('delete/<int:artist_id>', views.DeleteArtistAPI.as_view(), name='delete_artist'),
]