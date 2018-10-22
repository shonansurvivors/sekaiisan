from django.urls import path
from . import views


urlpatterns = [
    path('heritage/', views.HeritageListView.as_view(), name='heritage_list'),
    path('heritage/<str:name>/', views.HeritageArticleListView.as_view(), name='heritage_article_list'),
    path('area/<str:area>/', views.AreaCountryListView.as_view(), name='area_country_list'),
    path('country/<str:name>/', views.CountryHeritageListView.as_view(), name='country_heritage_list'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('about-us/', views.AboutUsView.as_view(), name='about-us'),
    path('', views.ArticleListView.as_view(), name='article_list'),
]