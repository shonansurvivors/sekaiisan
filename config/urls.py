from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from trip_app.sitemaps import (ArticleListSitemap,
                               HeritageListSitemap,
                               HeritageArticleListSitemap,
                               BlogArticleListSitemap,
                               CountryHeritageListSitemap,
                               )

sitemaps = {
    'article_list': ArticleListSitemap,
    'heritage_list': HeritageListSitemap,
    'heritage_article_list': HeritageArticleListSitemap,
    'blog_article_list': BlogArticleListSitemap,
    'country_heritage_list': CountryHeritageListSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('', include('trip_app.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
