from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new/', views.create_post, name='create_post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('like/<int:post_id>/', views.toggle_like, name='toggle_like'),
]
