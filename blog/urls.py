from django.urls import path
from .import views
from .views import PostListView,RebortListView,PostDetailView,RebortDetailView,PostCreateView,RebortCreateView,PostUpdateView,RebortUpdateView,PostDeleteView,RebortDeleteView,RebortListViewForM



urlpatterns = [
    path('',PostListView.as_view(),name='blog-home'),
    path('municipality/', views.municipality, name='municipality'),
    path('post/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    path('post/new/',PostCreateView.as_view(),name='post-create'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name='post-delete'),
    path('about/',views.about,name='blog-about'),
    path('myreborts/',RebortListView.as_view(),name='blog-myreborts'),
    path('myreborts/<int:pk>/',RebortDetailView.as_view(),name='rebort-detail'),
    path('myreborts/new/',RebortCreateView.as_view(),name='rebort-create'),
    path('myreborts/<int:pk>/update/',RebortUpdateView.as_view(),name='rebort-update'),
    path('myreborts/<int:pk>/delete/',RebortDeleteView.as_view(),name='rebort-delete'),
    path('myrebortsM/',RebortListViewForM.as_view(),name='blog-myrebortsM'),

    
]