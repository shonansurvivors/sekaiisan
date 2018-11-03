from django.contrib.sitemaps import Sitemap
from django.shortcuts import resolve_url
from .models import Heritage, Country


class ArticleListSitemap(Sitemap):

    changefreq = 'always'
    priority = 1.0
    protocol = 'https'

    def items(self):
        return ['index']

    def location(self, obj):
        return resolve_url('article_list')


class HeritageArticleListSitemap(Sitemap):

    changefreq = 'always'
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Heritage.objects.filter(article__word_count_per_image__gt=0, article__blog__hidden=False).distinct()

    def location(self, obj):
        return resolve_url('heritage_article_list', name=obj.formal_name)


class CountryHeritageListSitemap(Sitemap):

    changefreq = 'always'
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Country.objects.\
            filter(heritage__article__word_count_per_image__gt=0, heritage__article__blog__hidden=False).distinct()

    def location(self, obj):
        return resolve_url('country_heritage_list', name=obj.formal_name)
