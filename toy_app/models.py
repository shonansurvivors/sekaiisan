import json
from django.db import models


class Tag(models.Model):
    name = models.CharField(verbose_name='タグ名', max_length=255, unique=True)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    official_url = models.URLField(verbose_name='公式URL', blank=True, null=True)
    name = models.CharField(verbose_name='商品名', max_length=255)
    image = models.URLField(verbose_name='商品画像', blank=True, null=True)
    description = models.TextField(verbose_name='商品説明', blank=True, null=True)
    release_date = models.DateField(verbose_name='発売日', blank=True, null=True)
    proper_price = models.IntegerField(verbose_name='定価', blank=True, null=True)
    tag = models.ManyToManyField(Tag, verbose_name="タグ", blank=True, null=True)
    asin = models.CharField(verbose_name='ASIN', max_length=10, blank=True, null=True)
    amazon_url = models.URLField(verbose_name='Amazonアフィリエイト', blank=True, null=True)

    # url
    # caption
    # max_price
    # min_price
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    @classmethod
    def get_items_each_for_tags(cls):

        tags = Tag.objects.all()

        items_each_for_tags = []

        for tag in tags:

            items_each_for_tag = {}

            items_each_for_tag['tag'] = tag

            items = cls.objects.filter(tag=tag).order_by('-release_date')

            items_each_for_tag['items'] = []

            for item in items[:4]:

                items_each_for_tag['items'].append(item)

            items_each_for_tags.append(items_each_for_tag.copy())

        return items_each_for_tags

    def __str__(self):
        return self.name
