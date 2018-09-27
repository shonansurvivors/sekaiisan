from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('list/<int:tag_id>/', views.item_list, name='item_list'),
    path('detail/<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
]