from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>', views.room, name='room'),
    path('edit-user/<str:pk>', views.edit_user, name='edit_user'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('create-room/', views.create_room, name='create_room'),
    path('update-room/<str:pk>', views.update_room, name='update_room'),
    path('delete-room/<str:pk>', views.delete_room, name='delete_room'),
    path('delete-message/<str:pk>', views.delete_message, name='delete_message'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_page, name='register'),
    path('topics/', views.topics_page, name='topics'),
    path('activity/', views.activity_page, name='activity'),
]

