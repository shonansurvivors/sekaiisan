# Generated by Django 2.1 on 2018-10-01 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='heritage',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='国名'),
        ),
    ]
