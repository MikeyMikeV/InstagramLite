from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('registration', views.create_user, name='create_user'),
    path('activate/<uid>/<token>/', views.activate, name='activate'),
]