from django.core import serializers
import json
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from ...models import Item, Tag


class Command(BaseCommand):

    help = 'Export json file from toy_app.models.Item'

    def handle(self, *args, **kwargs):

        tags = Tag.objects.all()

        json_data = json.loads(serializers.serialize('json', tags, ensure_ascii=False))

        with open('model_data/tag.json', 'w', encoding='UTF-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

