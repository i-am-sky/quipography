from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('logout/', views.Customlogout, name='logout'),
    path('signup/', views.CustomSignup, name='signup'),
    path('create-post/', views.CreatePost, name='create-post'),
]
