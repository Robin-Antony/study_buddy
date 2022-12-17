from django.urls import path
from. import views


urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name = 'room'),
    path('create-room',views.createRoom,name='create-room'),
    path('update-room/<str:pk>/',views.updateRoom,name='updateRoom'),
    path('delete-romm/<str:pk>/', views.deleteRoom,name='delete-room'),
    path('login',views.loginPage, name='login'),
    path('logout',views.logoutPage, name='logout'),
    path('register', views.registerPage, name='register'),
    path('deleteMessage/<str:pk>/', views.deleteMessage, name='delete-message'),
    path('userProfile/<str:pk>/', views.userProfile,name='user-profile'),
    path('update-user', views.updateUser, name='update-user'),
    path('topic/',views.topic,name='topic'),
    path('activity/',views.activity, name='activity')

]