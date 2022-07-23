import json
from common import  remove_currency, generate_insert,generate_historical

import requests


class Aldi():

    historical = []
    products = []

    def __init__(self, catagories):

        self.catagories = catagories
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:85.0) Gecko/20100101 Firefox/85.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-GB',
            'Content-Type': 'application/json; charset=UTF-8',
            'WebsiteId': 'a763fb4a-0224-4ca8-bdaa-a33a4b47a026',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://groceries.aldi.ie',
            'Connection': 'keep-alive',
            'Referer': 'https://groceries.aldi.ie/en-GB/',
            'TE': 'Trailers',
        }

        self._params = (
            ('limit', '200'),
        )

        self.get_aldi_products()

    def get_aldi_products(self):

        for catagory in self.catagories:
            query = json.dumps({"Query": catagory})
            response = requests.post('https://groceries.aldi.ie/api/aldisearch/autocomplete', headers=self._headers,
                                     params=self._params, data=query)

            for item in response.json()['Suggestions']:
                data = ['NA', remove_currency(item['CurrentListPrice']), 'NA']
                url =f"https://groceries.aldi.ie{item['Url']}"
                sql = generate_insert(catagory, item['DisplayName'], 'Aldi', data,
                                      url=url, brand=item['Brand'],
                                      sku=item['Sku'])
                self.products.append(sql)
                self.historical.append(generate_historical(data, url))