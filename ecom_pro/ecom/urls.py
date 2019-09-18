from django.urls import path 
from . import views
from .views import PostListView,PostDetailView,add_to_cart

urlpatterns = [
    path('',views.PostListView.as_view(),name='ecom-home'),
    path('item/<int:pk>/',views.PostDetailView.as_view(), name="item-detail"),
    path('add_to_cart/<int:pk>/', add_to_cart, name="add-to-cart"),
    path('remove_from_cart/<int:pk>/', add_to_cart, name="remove-from-cart"),
    path('item/', views.item_list, name= 'item-list'),
    path('about/',views.about,name= 'ecom-about')
    
]
