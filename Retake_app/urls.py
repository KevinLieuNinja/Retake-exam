from django.urls import path
from . import views

urlpatterns= [
    path('', views.index),
    path('dash', views.dash),
    path('login', views.login),
    path('logout', views.logout),
    path('register', views.register),
    path('createThought',views.createThought),
    path('viewThought/<int:id>', views.viewThought),
    path('likedThought/<int:id>', views.likedThought),
    path('unlikeThought/<int:id>', views.unlikeThought),
    path('deleteThought/<int:id>',views.deleteThought),

]