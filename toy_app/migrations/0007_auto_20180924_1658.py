# Generated by Django 2.1 on 2018-09-24 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toy_app', '0006_auto_20180922_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.URLField(null=True, verbose_name='商品画像'),
        ),
    ]
