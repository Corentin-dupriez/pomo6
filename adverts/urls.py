from django.urls import path, include

from adverts import views

urlpatterns = [
    path('search/', views.ResultsView.as_view(), name='search_view'),
    path('new/', views.ListingCreateView.as_view(), name='create_ad_view'),
    path('<int:pk>/<slug:slug>', include(
        [path('', views.ListingView.as_view(), name='advert_view'),
         path('edit/', views.ListingUpdateView.as_view(), name='advert_edit')
         ]
    )
         )
]