from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name='blog-home'),
    path('municipality/', views.municipality, name='municipality'),
    path('about/',views.about,name='blog-about'),
]