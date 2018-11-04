import random
import re
from time import sleep

from bs4 import BeautifulSoup
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.utils import IntegrityError
import requests

from .bing import Bing
from .heritage import get_heritage_regex


class SiteMaster(models.Model):
    description = models.TextField(verbose_name='サイト説明文', blank=True, null=True)
    contact_form_utl = models.URLField(verbose_name='お問い合わせフォームURL', blank=True, null=True)
    dummy = models.TextField(verbose_name='dummy', blank=True, null=True)


class Country(models.Model):
    formal_name = models.CharField(verbose_name='正式名称', max_length=255, db_index=True, blank=True, null=True)
    short_name = models.CharField(verbose_name='通称', max_length=255, blank=True, null=True)
    area_choices = (
        ('EU', 'ヨーロッパ'),
        ('AS', 'アジア'),
        ('NA', '北米・中米'),
        ('SA', '南米'),
        ('OC', 'オセアニア'),
        ('AF', 'アフリカ'),
    )
    area = models.CharField(verbose_name='地域', max_length=2, choices=area_choices, null=True)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    class Meta:
        ordering = ('short_name',)

    def __str__(self):
        return self.short_name


class Heritage(models.Model):
    formal_name = models.CharField(verbose_name='名称', max_length=255, db_index=True)
    country = models.ForeignKey(Country, verbose_name='国', on_delete=models.SET_NULL, null=True)
    regex = models.CharField('正規表現', max_length=255, blank=True, null=True)
    description = models.TextField(verbose_name='説明文', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    class Meta:
        ordering = ('formal_name',)

    def __str__(self):
        return self.formal_name

    @classmethod
    def scraping_all(cls):

        urls = [
            'http://www.unesco.or.jp/isan/list/europe_1/',
            'http://www.unesco.or.jp/isan/list/europe_2/',
            'http://www.unesco.or.jp/isan/list/europe_3/',
            'http://www.unesco.or.jp/isan/list/asia_1/',
            'http://www.unesco.or.jp/isan/list/asia_2/',
            'http://www.unesco.or.jp/isan/list/america_1/',
            'http://www.unesco.or.jp/isan/list/america_2/',
            'http://www.unesco.or.jp/isan/list/oceania/',
            'http://www.unesco.or.jp/isan/list/africa/',
        ]

        for url in urls:

            print(url)
            sleep(1)
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'lxml')

            element_tags = soup.find_all('th')

            for element_tag in element_tags:

                if element_tag.text == '遺跡名称':
                    continue

                # 項番かどうか判定
                if len(element_tag.text) <= 2:
                    continue

                if re.search('登録削除', element_tag.text):
                    continue

                # 世界遺産名をURLに含めている為、半角スラッシュを全角に変換しておく
                heritage_name = element_tag.text.rstrip().replace('/', '／')

                try:
                    heritage = cls.objects.get(formal_name=heritage_name)
                except ObjectDoesNotExist:
                    heritage = Heritage()
                    heritage.formal_name = heritage_name

                try:
                    country_name = element_tag.find_parent().find_parent().find_parent('table')['summary']

                    try:
                        country = Country.objects.get(formal_name=country_name)
                    except ObjectDoesNotExist:
                        country = Country()

                    country.formal_name = country_name

                    if 'europe' in url:
                        country.area = 'EU'
                    elif 'asia' in url:
                        country.area = 'AS'
                    elif 'america_1' in url:
                        country.area = 'NA'
                    elif 'america_2' in url:
                        country.area = 'SA'
                    elif 'oceania' in url:
                        country.area = 'OC'
                    elif 'africa' in url:
                        country.area = 'AF'
                    else:
                        country.area = None

                    country.save()

                    heritage.country = country

                except TypeError:
                    pass

                heritage.save()

        cls.update_regex_all()

    @classmethod
    def update_regex_all(cls):

        heritages = cls.objects.all()

        for heritage in heritages:

            heritage.regex = get_heritage_regex(heritage.formal_name)
            heritage.save()

    @classmethod
    def put_text(cls):

        heritages = cls.objects.all().order_by('formal_name')

        heritage_list = list()

        for heritage in heritages:
            work_list = list()
            work_list.append(str(heritage.formal_name))
            work_list.append(str(heritage.regex))
            heritage_list.append(work_list.copy())

        with open('heritage.txt', 'w', encoding='UTF-8') as f:
            print('[', file=f)
            for heritage in heritage_list:
                print(f'    {heritage},', file=f)
            print(']', file=f)


class Blog(models.Model):
    domain = models.URLField(verbose_name='ドメイン', unique=True)
    title = models.CharField(verbose_name='タイトル', max_length=255, blank=True, null=True)
    author_name = models.CharField(verbose_name='筆者名', max_length=255, blank=True, null=True)
    author_id = models.CharField(verbose_name='筆者ID', max_length=255, blank=True, null=True)
    hidden = models.BooleanField(verbose_name='非表示', default=False)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

    @classmethod
    def delete_garbage(cls):

        print(f'delete_garbage run.')

        num = cls.objects.filter(article__isnull=True).count()

        cls.objects.filter(article__isnull=True).delete()

        print(f'delete {num} blogs ')


class Article(models.Model):
    url = models.CharField(verbose_name='URL', max_length=2048, unique=True)
    title = models.CharField(verbose_name='タイトル', max_length=255, blank=True, null=True)
    text = models.TextField(verbose_name='本文', blank=True, null=True)
    word_count = models.IntegerField(verbose_name='字数', blank=True, default=0)
    image_count = models.IntegerField(verbose_name='画像数', blank=True, default=0)
    word_count_per_image = models.IntegerField(verbose_name='画像あたり字数', db_index=True, blank=True, default=0)
    heritage = models.ManyToManyField(Heritage, verbose_name="世界遺産", blank=True)
    blog = models.ForeignKey(Blog, verbose_name='ブログ', on_delete=models.SET_NULL, null=True)
    hidden = models.BooleanField(verbose_name='非表示', default=False)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    @classmethod
    def update_word_count_per_image_all(cls):

        articles = cls.objects.all()

        for article in articles:

            if article.image_count:
                article.word_count_per_image = article.word_count // article.image_count
                article.save()

    def update_heritage(self, heritages=None):

        print(f'update_heritage run. Article.pk: {self.pk} title: {self.title}')

        if heritages is None:
            heritages = Heritage.objects.all()

        self.heritage.clear()

        if self.text:

            for heritage in heritages:

                # print(heritage.regex)

                if re.search(heritage.regex, self.text):
                    self.heritage.add(heritage)
                    print(f'Article.heritage add. heritage: {heritage.formal_name}')

            self.save()

    @classmethod
    def update_heritage_all(cls):

        articles = cls.objects.all()
        heritages = Heritage.objects.all()

        for article in articles:

            print(f'update_heritage run. Article.pk: {article.pk} title: {article.title}')

            # 500字未満のブログ記事は対象外とし効率化
            if article.word_count >= 500:

                article.heritage.clear()

                for heritage in heritages:

                    if re.search(heritage.regex, article.text):
                        article.heritage.add(heritage)
                        print(f'Article.heritage add. heritage: {heritage.formal_name}')

                article.save()

            else:
                print('word_count is less than 1000')

    def scraping_content(self):

        print(f'scraping_content run. Article.pk: {self.pk} url: {self.url}')

        sleep(1)
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, 'html.parser')

        try:
            if soup.html.get('data-admin-domain') == '//blog.hatena.ne.jp':
                self.title = soup.find(class_='entry-title').text

                try:
                    self.text = soup.find_all(class_='entry-content')[-1].text
                    self.word_count = len(soup.find_all(class_='entry-content')[-1].text)
                    self.image_count = len(soup.find_all(class_='entry-content')[-1].find_all('img'))
                    if self.image_count:
                        self.word_count_per_image = self.word_count // self.image_count

                    blog_domain = soup.html.get('data-blog-host')

                    if blog_domain:

                        try:
                            blog = Blog.objects.get(domain=blog_domain)

                        except ObjectDoesNotExist:
                            blog = Blog()
                            blog.domain = blog_domain

                        blog.title = soup.html.get('data-blog-name')
                        blog.author_name = soup.html.get('data-blog-owner')
                        blog.author_id = blog.author_name
                        blog.save()

                        self.blog = blog
                        print(f'Blog is created or updated. pk: {blog.pk} title: {blog.title}')

                    self.save()
                    print(f'Article is updated. title: {self.title}')

                    self.update_heritage()

                except IndexError:
                    print(f'BeautifulSoup: IndexError(entry-content is not found)')

        except AttributeError:
            print(f'BeautifulSoup: AttributeError')

    @classmethod
    def scraping_content_all(cls):

        articles = cls.objects.all()
        for article in articles:

            if article.title:
                if 0 < article.word_count < 1000:
                    continue

            article.scraping_content()

    @classmethod
    def scraping_url(cls, url):

        # bing = Bing()
        # urls = bing.get_urls(required_url_number=5000)

        article = Article()
        article.url = url

        try:
            article.save()
            print(f'Article is created. url:{url}')

            article.scraping_content()

        except IntegrityError:
            print(f'Article is not created.IntegrityError. url: {url}')

    @classmethod
    def scraping_uncollected_heritage(cls):

        print(f'scraping_uncollected_heritage run.')

        bing = Bing()
        heritages = Heritage.objects.filter(article__isnull=True)

        # 検索ワードが長すぎるとヒットしない？かもしれないので10文字までにしてみる
        bing.keywords = ['世界遺産', '旅', heritages[random.randrange(len(heritages))].formal_name[:10]]

        bing.domains = ['hatenablog.com/entry']

        print(f'bing.keywords: {bing.keywords}')

        urls = bing.get_urls(required_url_number=50)

        for url in urls:

            article = Article()
            article.url = url

            try:
                article.save()
                print(f'Article is created. url:{url}')

                article.scraping_content()

            except IntegrityError:
                print(f'Article is not created.IntegrityError. url: {url}')

        article_count = Article.objects.filter(word_count_per_image__gt=0, heritage__isnull=False, blog__hidden=False).distinct().count()
        print(f'article_count:{article_count}')

    @classmethod
    def cut_text(cls):

        print(f'cut_text run.')

        articles = cls.objects.all()

        for article in articles:
            article.text = article.text[:200]
            article.save()

    @classmethod
    def delete_garbage(cls):

        print(f'delete_garbage run.')

        num = cls.objects.filter(heritage__isnull=True).count()

        cls.objects.filter(heritage__isnull=True).delete()

        print(f'delete {num} articles ')