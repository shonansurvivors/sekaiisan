import re
from time import sleep

from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.utils import IntegrityError
import requests

from .bing import Bing


class SiteMaster(models.Model):
    description = models.TextField(verbose_name='サイト説明文', blank=True, null=True)


class Country(models.Model):
    formal_name = models.CharField(verbose_name='正式名称', max_length=255, blank=True, null=True)
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

    def __str__(self):
        return self.formal_name


class Heritage(models.Model):
    formal_name = models.CharField(verbose_name='名称', max_length=255)
    country = models.ForeignKey(Country, verbose_name='国', on_delete=models.SET_NULL, null=True)
    regex = models.CharField('正規表現', max_length=255, blank=True, null=True)
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

        with open('heritage.txt', 'w', encoding='UTF-8') as f:

            for heritage in heritages:

                t = heritage.formal_name

                t = t.replace('を含むスタッドリー王立公園', '、スタッドリー王立公園')
                t = t.replace('エーヴベリーと関連する遺跡', 'エーヴベリー')
                t = t.replace('スピシュスキー城及びその関連する文化財', 'スピシュスキー城')
                t = t.replace('ベリンツォーナ旧市街にある3つの城、要塞及び城壁',
                              'ベリンツォーナ旧市街、カステルグランデ、モンテベッロ城、サッソ・コルバロ城')
                t = t.replace('オフリド地域の自然遺産及び文化遺産', 'オフリド地域の自然遺産及びオフリド地域の文化遺産')
                t = t.replace('デルベントのシタデル、古代都市、要塞建築物群', 'デルベントのシタデル、アレクサンドロスの門')
                t = t.replace('ポーランド、ウクライナのカルパチア地方の木造教会', 'カルパチア地方の木造教会')
                # ルルーはレンタルルームなどにヒットする為、削除
                t = t.replace('及びル・ルー（エノー）', '')
                t = t.replace('ネースヴィジのラジヴィール家の建築、住居、文化的複合体', 'ネースヴィジのラジヴィール家')
                # バットは野球のバットなどにヒットする為、削除
                t = t.replace('バット、アル-フトゥム、アル-アインの古代遺跡群', 'アル-フトゥム、アル-アイン')
                t = t.replace('明治日本の産業革命遺産　製鉄・製鋼、造船、石炭産業', '明治日本の産業革命遺産')
                t = t.replace('平泉-仏国土（浄土）を表す建築・庭園及び考古学的遺跡群', '平泉')
                t = t.replace('ポルトヴェネーレ、チンクエ・テッレ及び小島群（パルマリア、ティーノ及びティネット島）',
                              'ポルトヴェネーレ、チンクエ・テッレ、パルマリア、ティーノ、ティネット')
                t = t.replace('アントニ・ガウディの作品群', 'ガウディ')
                t = t.replace('富士山－信仰の対象と芸術の源泉', '富士山')
                t = t.replace('富岡製糸場と絹産業遺産群', '富岡製糸場')
                t = t.replace('法隆寺地域の仏教建造物', '法隆寺')
                t = t.replace('琉球王国のグスク及び関連遺産群', '琉球王国のグスク')
                t = t.replace('紀伊山地の霊場と参詣道', '紀伊山地の霊場')
                t = t.replace('アウシュヴィッツ・ビルケナウ　ナチスドイツの強制絶滅収容所（1940 - 1945）',
                              'アウシュヴィッツ・ビルケナウ　ナチスドイツの強制絶滅収容所')
                t = t.replace('ケニア山国立公園／自然林', 'ケニア山国立公園')

                t = t.replace('国立公園', '(国立)?公園')
                t = t.replace('王立公園', '(王立)?公園')
                t = t.replace('・', '・?')
                t = t.replace('-', '[-・]?')
                t = t.replace('の', 'の?')

                t = t.replace('及び', '、')
                t = re.sub(r'(\s)+', '、', t)
                t = re.sub(r'(　)+', '、', t)
                t = t.replace('／', '、')
                t = t.replace('（', '(')
                t = t.replace('）', ')?')
                t = t.replace('：', '、')

                t = t.replace('、、', '、')

                if '、' in t:
                    t = f'({t.replace("、","|")})'

                f.write(heritage.formal_name + '\n')
                f.write(t + '\n')

                heritage.regex = t
                heritage.save()


class Blog(models.Model):
    domain = models.URLField(verbose_name='ドメイン', unique=True)
    title = models.CharField(verbose_name='タイトル', max_length=255, blank=True, null=True)
    author_name = models.CharField(verbose_name='筆者名', max_length=255, blank=True, null=True)
    author_id = models.CharField(verbose_name='筆者ID', max_length=255, blank=True, null=True)
    hidden = models.BooleanField(verbose_name='非表示', default=False)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class Article(models.Model):
    url = models.CharField(verbose_name='URL', max_length=2048, unique=True)
    title = models.CharField(verbose_name='タイトル', max_length=255, blank=True, null=True)
    text = models.TextField(verbose_name='本文', blank=True, null=True)
    word_count = models.IntegerField(verbose_name='字数', blank=True, default=0)
    image_count = models.IntegerField(verbose_name='画像数', blank=True, default=0)
    word_count_per_image = models.IntegerField(verbose_name='画像あたり字数', blank=True, default=0)
    heritage = models.ManyToManyField(Heritage, verbose_name="世界遺産", blank=True)
    blog = models.ForeignKey(Blog, verbose_name='ブログ', on_delete=models.SET_NULL, null=True)
    hidden = models.BooleanField(verbose_name='非表示', default=False)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.url

    @classmethod
    def update_word_count_per_image_all(cls):

        articles = cls.objects.all()

        for article in articles:

            if article.image_count:
                article.word_count_per_image = article.word_count // article.image_count
                article.save()

    def update_heritage(self, heritages=None):

        if heritages is None:
            heritages = Heritage.objects.all()

        self.heritage.clear()

        if self.text:

            for heritage in heritages:

                if re.search(heritage.regex, self.text):
                    self.heritage.add(heritage)

            self.save()

    @classmethod
    def update_heritage_all(cls):

        articles = cls.objects.all()
        heritages = Heritage.objects.all()

        for article in articles:

            article.update_heritage(heritages=heritages)

    def scraping_content(self):

        print(f'{self.pk}:{self.url}')

        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, 'lxml')

        try:
            if soup.html.get('data-admin-domain') == '//blog.hatena.ne.jp':
                self.title = soup.find(class_='entry-title').text
                self.text = soup.find(class_='entry-content').text
                self.word_count = len(soup.find(class_='entry-content').text)
                self.image_count = len(soup.find(class_='entry-content').find_all('img'))
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

                    print(blog.title)

                self.save()

                self.update_heritage()

        except AttributeError:
            print('AttributeError')

        print(f'{self.title}')

    @classmethod
    def scraping_content_all(cls):

        articles = cls.objects.all()
        for article in articles:

            if article.title:
                if 0 < article.word_count < 1000:
                    continue

            sleep(0.5)
            article.scraping_content()

    @classmethod
    def scraping_url(cls):

        bing = Bing()
        urls = bing.get_urls(required_url_number=5000)

        for url in urls:

            article = Article()
            article.url = url

            try:
                article.save()
            except IntegrityError:
                pass
