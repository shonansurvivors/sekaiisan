# Generated by Django 2.1 on 2018-10-19 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trip_app', '0008_auto_20181019_1306'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.URLField(unique=True, verbose_name='ドメイン')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='タイトル')),
                ('author_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='筆者名')),
                ('author_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='筆者ID')),
                ('hidden', models.BooleanField(default=False, verbose_name='非表示')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ('-word_count_per_image',)},
        ),
        migrations.AddField(
            model_name='article',
            name='blog',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='trip_app.Blog', verbose_name='ブログ'),
        ),
    ]
