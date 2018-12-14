import random
from django.core.management.base import BaseCommand
from ...models import Heritage

class Command(BaseCommand):

    help = 'Scraping articles of uncollected heritage'

    def handle(self, *args, **kwargs):

        heritages = Heritage.objects.filter(article__isnull=True).distinct()
        heritage = heritages[random.randrange(len(heritages))]

        print(heritage.formal_name)
