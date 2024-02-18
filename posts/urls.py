from django.urls import path
from . import views
urlpatterns = [
    path('detail/<int:pid>/', views.post_detail, name = 'post_detail'),
    path('new/', views.post_new, name = 'post_new'),
    path('edit/<int:pid>/', views.post_edit, name = 'post_edit'),
    path('like/<int:pid>/<int:pfid>/', views.like_post, name='like_post')
]