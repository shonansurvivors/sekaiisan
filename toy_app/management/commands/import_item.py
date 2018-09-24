import json
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from ...models import Item


class Command(BaseCommand):

    help = 'Create Item from json file'

    def handle(self, *args, **kwargs):

        with open('b-boys.json', 'r') as f:

            data = json.load(f)
            create_count = 0
            update_count = 0

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
                item.image = item_obj['image']

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