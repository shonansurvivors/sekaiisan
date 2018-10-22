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

        with open('scraping_data/input/b-boys.json', 'r', encoding='UTF-8') as f:

            data = json.load(f)

        for item_obj in data:

            item_obj['date'] = datetime.strptime(item_obj['date'], '発売日：%Y年%m月%d日')

        with open('scraping_data/b-boys.json', 'w', encoding='UTF-8') as f:
            json.dump(data, f, default=support_datetime_default, ensure_ascii=False, indent=4)
