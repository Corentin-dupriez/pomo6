from django.urls import path

from profiles import views
from profiles.views import register_view, ProfileView

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', register_view, name='register'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
]