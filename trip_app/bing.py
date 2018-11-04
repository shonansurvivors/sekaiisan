import math
from time import sleep
from urllib import parse

import requests


class Bing:

    def __init__(self):

        self.keywords = ['世界遺産', '旅行']
        self.domains = ['hatenablog.jp']
        self.urls = []

    def get_urls(self, required_url_number=50):

        print(f'get_urls run.')

        # ex) edited_keywords = '世界遺産 旅行'
        edited_keywords = ''
        for i, keyword in enumerate(self.keywords, 1):
            edited_keywords += keyword
            if i != len(self.keywords):
                edited_keywords += ' '
            else:
                pass
                # edited_keywords += ' -はてなブックマーク -はてなキーワード'

        # ex) edited_domains = '(site:hatenablog.com OR hatenablog.jp OR hateblo.jp)'
        edited_domains = '(site:'
        for i, domain in enumerate(self.domains, 1):
            edited_domains += domain
            if i != len(self.domains):
                edited_domains += ' OR '
            else:
                edited_domains += ')'

        search_term = f'{edited_keywords}{edited_domains}'

        # 欲しいURLの数
        required_url_number = required_url_number

        # 1回のレスポンスで返される結果の数(最大50)
        count = 50

        request_times = math.floor(required_url_number / count)

        subscription_key = '2c593047e951422b9777b1251059882a'
        search_url = 'https://api.cognitive.microsoft.com/bing/v7.0/search'
        headers = {"Ocp-Apim-Subscription-Key": subscription_key}

        self.urls = []
        for i in range(request_times):

            params = parse.urlencode(
                {"q": search_term,
                 "count": count,
                 "offset": count * i}
                )

            sleep(0.5)
            response = requests.get(search_url, headers=headers, params=params)
            response.raise_for_status()
            search_results = response.json()

            try:
                for value in search_results['webPages']['value']:
                    self.urls.append(value['url'])
                    print(value['url'])
            except KeyError:
                print('KeyError')

        return self.urls