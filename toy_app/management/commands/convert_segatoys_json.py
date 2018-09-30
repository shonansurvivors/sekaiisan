import json
from datetime import datetime
from django.core import serializers
from django.core.management.base import BaseCommand


def support_datetime_default(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(repr(o) + " is not JSON serializable")


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        with open('scraping_data/input/segatoys.json', 'r', encoding='UTF-8') as f:

            data = json.load(f)

        for item_obj in data:

            '''
            改行など除去
            '''
            item_obj['name'] = item_obj['name'].replace('\n', ' ')

            item_obj['price'] = item_obj['price'].replace('希望小売価格\n¥', '').replace(',', '')

            try:
                item_obj['date'] = datetime.strptime(item_obj['date'].replace(' 発売予定', ''), '%Y年%m月%d日')
            except KeyError:
                pass

        with open('scraping_data/output/segatoys.json', 'w', encoding='UTF-8') as f:
            json.dump(data, f, default=support_datetime_default, ensure_ascii=False, indent=4)
