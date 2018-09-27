import json
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from ...models import Item, Tag


class Command(BaseCommand):

    help = 'Create Item from json file'

    def handle(self, *args, **kwargs):

        with open('scraping_data/b-boys.json', 'r') as f:

            data = json.load(f)
            create_count = 0
            update_count = 0

            '''
            全データのタグを調べ、タグテーブルに未登録のものは登録する。
            '''
            for item_obj in data:

                for tag_name in item_obj['tags']:

                    try:
                        Tag.objects.get(name=tag_name)
                    except ObjectDoesNotExist:
                        tag = Tag()
                        tag.name = tag_name
                        tag.save()

            for item_obj in data:

                create_flg = False
                update_flg = False

                try:
                    item = Item.objects.get(official_url=item_obj['url'])

                    update_flg = True

                except ObjectDoesNotExist:
                    item = Item()
                    item.official_url = item_obj['url']

                    create_flg = True

                item.name = item_obj['name']

                '''
                if item_obj['image']:
                    item.image = item_obj['image']

                if not item.image:
                    print(f'Item: {item.id} has no image.')
                '''

                if item_obj['date']:
                    try:
                        item.release_date = datetime.datetime.strptime(item_obj['date'], '%Y-%m-%dT%H:%M:%S')
                    except ValueError:
                        pass

                for tag_name in item_obj['tags']:
                    try:
                        item.tag.add(Tag.objects.get(name=tag_name))
                    except ObjectDoesNotExist:
                        pass

                item.save()

                if create_flg:

                    print(f'Create Item: {item.id}: {item.name}')
                    create_count += 1

                elif update_flg:

                    print(f'Update Item: {item.id}: {item.name}')
                    update_count += 1

                else:
                    pass

            print(f'{create_count} items have been created.')
            print(f'{update_count} items have been updated.')