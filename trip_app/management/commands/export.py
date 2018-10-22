import json
from django.core import serializers
from django.core.management.base import BaseCommand
from ...models import SiteMaster, Country, Heritage, Blog, Article


class Command(BaseCommand):

    help = 'Export json file from trip_app.models'

    def handle(self, *args, **kwargs):

        items = SiteMaster.objects.all()
        json_data = json.loads(serializers.serialize('json', items, ensure_ascii=False))
        with open('trip_app/model_data/export/site_master.json', 'w', encoding='UTF-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

        items = Country.objects.all()
        json_data = json.loads(serializers.serialize('json', items, ensure_ascii=False))
        with open('trip_app/model_data/export/country.json', 'w', encoding='UTF-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

        items = Heritage.objects.all()
        json_data = json.loads(serializers.serialize('json', items, ensure_ascii=False))
        with open('trip_app/model_data/export/heritage.json', 'w', encoding='UTF-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

        items = Blog.objects.all()
        json_data = json.loads(serializers.serialize('json', items, ensure_ascii=False))
        with open('trip_app/model_data/export/blog.json', 'w', encoding='UTF-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

        items = Article.objects.all()
        json_data = json.loads(serializers.serialize('json', items, ensure_ascii=False))
        with open('trip_app/model_data/export/article.json', 'w', encoding='UTF-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
