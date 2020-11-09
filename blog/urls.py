from django.urls import path
from . import views
from users import views as users_view

app_name='blog'

urlpatterns = [
    path('',views.PostListView.as_view(),name='blog-home'),
    path('post-detail/<uuid:pk>',views.PostDetailView.as_view(),name='post-detail'),
    path('user/<str:username>',users_view.ProfileDetailView.as_view(),name='profile'),
    path('post/new/',views.PostCreateView.as_view(),name='post-new'),
    path('post/update/<uuid:pk>',views.PostUpdateView.as_view(),name='post-update'),
    path('post/delete/<uuid:pk>',views.PostDeleteView.as_view(),name='post-delete'),
]