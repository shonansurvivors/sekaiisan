# Generated by Django 2.1 on 2018-10-22 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip_app', '0015_auto_20181023_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='url',
            field=models.CharField(max_length=2048, unique=True, verbose_name='URL'),
        ),
    ]
