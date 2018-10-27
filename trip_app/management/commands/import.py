from django.core.management.base import BaseCommand
from django.core import serializers


class Command(BaseCommand):

    help = 'Create trip_app.models from json file'

    def handle(self, *args, **kwargs):

        '''
        with open('trip_app/model_data/import/site_master.json', 'r') as f:

            print('SiteMaster')
            data = f.read()
            count = 0
            for obj in serializers.deserialize('json', data):
                obj.save()
                count += 1
            print(f'{count} objects have been imported.')
        '''

        with open('trip_app/model_data/import/country.json', 'r') as f:

            print('Country')
            data = f.read()
            count = 0
            for obj in serializers.deserialize('json', data):
                obj.save()
                count += 1
            print(f'{count} objects have been imported.')

        with open('trip_app/model_data/import/heritage.json', 'r') as f:

            print('Heritage')
            data = f.read()
            count = 0
            for obj in serializers.deserialize('json', data):
                obj.save()
                count += 1
            print(f'{count} objects have been imported.')

        with open('trip_app/model_data/import/blog.json', 'r') as f:

            print('Blog')
            data = f.read()
            count = 0
            for obj in serializers.deserialize('json', data):
                obj.save()
                count += 1
            print(f'{count} objects have been imported.')

        with open('trip_app/model_data/import/article.json', 'r') as f:

            print('Article')
            data = f.read()
            count = 0
            for obj in serializers.deserialize('json', data):
                obj.save()
                count += 1
            print(f'{count} objects have been imported.')
