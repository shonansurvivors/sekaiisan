# Generated by Django 2.1 on 2018-10-20 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip_app', '0011_sitemaster'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='area',
            field=models.CharField(choices=[('EU', 'ヨーロッパ'), ('AS', 'アジア'), ('NA', '北米・中米'), ('SA', '南米'), ('OC', 'オセアニア'), ('AF', 'アフリカ')], max_length=2, null=True, verbose_name='地域'),
        ),
    ]
