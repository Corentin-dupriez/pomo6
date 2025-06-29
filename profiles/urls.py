from django.urls import path, include

from profiles import views
from profiles.views import register_view, ProfileView, ProfileEditView

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', register_view, name='register'),
    path('profile/<int:pk>/', include(
        [path('', ProfileView.as_view(), name='profile'),
         path('edit/', ProfileEditView.as_view(), name='profile-edit'),]
    )),
]