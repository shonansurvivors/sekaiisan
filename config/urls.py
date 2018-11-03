from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from trip_app.sitemaps import ArticleListSitemap, HeritageArticleListSitemap, CountryHeritageListSitemap

sitemaps = {
    'article_list': ArticleListSitemap,
    'heritage_article_list': HeritageArticleListSitemap,
    'country_heritage_list': CountryHeritageListSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('', include('trip_app.urls')),
]
