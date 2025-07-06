from django.urls import path

from chat import views

urlpatterns = [
    path('', views.ThreadListView.as_view(), name='thread-list'),
    path('<int:pk>/', views.ThreadDetailView.as_view(), name='thread-detail'),
    path('find_chat/<int:advert_id>/', views.ThreadRedirectView.as_view(), name='thread-redirect'),
]