from django.urls import path
from django.views.decorators.cache import cache_page
from . import views


urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('area/<str:area>/', cache_page(60 * 15)(views.AreaCountryListView.as_view()), name='area_country_list'),
    path('country/<str:name>/', views.CountryHeritageListView.as_view(), name='country_heritage_list'),
    path('heritage/', cache_page(60 * 15)(views.HeritageListView.as_view()), name='heritage_list'),
    path('heritage/<str:name>/', views.HeritageArticleListView.as_view(), name='heritage_article_list'),
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>', views.BlogArticleListView.as_view(), name='blog_article_list'),
    # path('contact/', views.ContactView.as_view(), name='contact'),
    path('about-us/', views.AboutUsView.as_view(), name='about-us'),
    path('nonheritage/', views.NonArticleHeritageListView.as_view(), name='nonheritage_list'),
]