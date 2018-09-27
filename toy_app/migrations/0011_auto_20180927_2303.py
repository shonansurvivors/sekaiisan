# Generated by Django 2.1 on 2018-09-27 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toy_app', '0010_auto_20180925_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='proper_price',
            field=models.IntegerField(blank=True, null=True, verbose_name='定価'),
        ),
        migrations.AddField(
            model_name='item',
            name='release_date',
            field=models.DateField(blank=True, null=True, verbose_name='発売日'),
        ),
    ]
