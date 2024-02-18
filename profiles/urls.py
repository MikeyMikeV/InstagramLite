from django.urls import path
from . import views
urlpatterns = [
    path('detail/<uid>/', views.profile_detail, name='profile_detail'),
]