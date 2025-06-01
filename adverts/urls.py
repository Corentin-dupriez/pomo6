from django.urls import path, include

from adverts import views

urlpatterns = [
    path('search/', views.search_view, name='search_view'),
    path('new/', views.create_ad_view, name='create_ad_view'),
    path('<int:pk>/<slug:slug>', include(
        [path('', views.advert_view, name='advert_view'),
         path('edit/', views.advert_view, name='advert_edit'),]))
]