import datetime
from django.contrib.sitemaps import Sitemap
from django.shortcuts import resolve_url
from .models import Heritage, Country, Blog


class ArticleListSitemap(Sitemap):

    changefreq = 'weekly'
    priority = 1.0
    protocol = 'https'
    lastmod = datetime.datetime.strptime('2018/11/21', '%Y/%m/%d')

    def items(self):
        return ['index']

    def location(self, obj):
        return resolve_url('article_list')


class HeritageListSitemap(Sitemap):

    changefreq = 'weekly'
    priority = 0.3
    protocol = 'https'
    lastmod = datetime.datetime.strptime('2018/11/21', '%Y/%m/%d')

    def items(self):
        return ['index']

    def location(self, obj):
        return resolve_url('heritage_list')


class HeritageArticleListSitemap(Sitemap):

    changefreq = 'weekly'
    priority = 1.0
    protocol = 'https'
    lastmod = datetime.datetime.strptime('2018/11/21', '%Y/%m/%d')

    def items(self):
        return Heritage.objects.\
            filter(article__word_count_per_image__gt=0, article__isnull=False, article__blog__hidden=False).distinct()

    def location(self, obj):
        return resolve_url('heritage_article_list', name=obj.formal_name)


class BlogArticleListSitemap(Sitemap):

    changefreq = 'weekly'
    priority = 1.0
    protocol = 'https'
    lastmod = datetime.datetime.strptime('2018/11/21', '%Y/%m/%d')

    def items(self):
        return Blog.objects.\
            filter(article__word_count_per_image__gt=0, article__heritage__isnull=False, hidden=False).distinct()

    def location(self, obj):
        return resolve_url('blog_article_list', pk=obj.pk)


class CountryHeritageListSitemap(Sitemap):

    changefreq = 'weekly'
    priority = 0.3
    protocol = 'https'
    lastmod = datetime.datetime.strptime('2018/11/21', '%Y/%m/%d')

    def items(self):
        return Country.objects.\
            filter(heritage__article__word_count_per_image__gt=0, heritage__article__blog__hidden=False).distinct()

    def location(self, obj):
        return resolve_url('country_heritage_list', name=obj.formal_name)
