import json
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.core import serializers
from ...models import Item, Tag


class Command(BaseCommand):

    help = 'Create Tag from json file'

    def handle(self, *args, **kwargs):

        with open('model_data/import/tag.json', 'r') as f:

            data = f.read()

            count = 0
            for obj in serializers.deserialize('json', data):
                obj.save()
                count += 1

            print(f'{count} tags have been imported.')
