from django.urls import path, include

from adverts import views
from adverts.views import PredictCategoryView

urlpatterns = [
    path('search/', views.ResultsView.as_view(), name='search_view'),
    path('my-listings/', views.MyListingsView.as_view(), name='my_listings'),
    path('to-approve/', views.ListingsToApproveView.as_view(), name='to_approve'),
    path('new/', views.ListingCreateView.as_view(), name='create_ad_view'),
    path('<int:pk>/<slug:slug>/', include(
        [path('', views.ListingView.as_view(), name='advert_view'),
         path('edit/', views.ListingUpdateView.as_view(), name='advert_edit')
         ],
    ),
         ),
    path('api/predict-category/', PredictCategoryView.as_view(), name='predict_category'),
]