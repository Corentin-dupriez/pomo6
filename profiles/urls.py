from django.urls import path

from profiles import views
from profiles.views import register_view

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', register_view, name='register'),
]