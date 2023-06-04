from .import views
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterUserAPI.as_view(), name='register_user'),
    path('list/', views.ListUsersAPI.as_view(), name='list_users'),
    path('update/<int:user_id>', views.UpdateUserAPI.as_view(), name='list_users'),
    path('delete/<int:user_id>', views.UpdateUserAPI.as_view(), name='list_users'),
]