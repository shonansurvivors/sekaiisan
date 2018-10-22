import json
import math
from urllib import parse

import requests


class Bing:

    def __init__(self):

        self.search_term = '"世界遺産"+"旅行"(site:hatenablog.com OR hatenablog.jp OR hateblo.jp OR hatenadiary.com OR hatenadiary.jp)'
        self.urls = []

    def get_urls(self, required_url_number=100):

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
                {"q": self.search_term,
                 "count": count,
                 "offset": count * i}
                )

            response = requests.get(search_url, headers=headers, params=params)
            response.raise_for_status()
            search_results = response.json()

            for value in search_results['webPages']['value']:
                self.urls.append(value['url'])

        return self.urls