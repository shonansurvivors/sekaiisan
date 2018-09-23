from django.db import models


class Tag(models.Model):
    name = models.CharField(verbose_name='タグ名', max_length=255, unique=True)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(verbose_name='商品名', max_length=255)
    image = models.URLField(verbose_name='商品画像')
    description = models.TextField(verbose_name='商品説明', null=True)
    tag = models.ManyToManyField(Tag, verbose_name="タグ", blank=True)
    # url
    # caption
    # max_price
    # min_price
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name
