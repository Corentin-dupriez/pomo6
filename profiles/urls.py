from django.urls import path, include

from profiles import views
from profiles.views import ProfileView, ProfileEditView

urlpatterns = [
    path('profile/<int:pk>/', include(
        [path('', ProfileView.as_view(), name='profile'),
         path('edit/', ProfileEditView.as_view(), name='profile-edit'),]
    )),
]