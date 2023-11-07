import json
from common import standardise, generate_insert, replace_ownbrand

import requests


class Aldi:

    _headers = {
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

    _params = (
        ('limit', '200'),
    )

    def format_dict(self, product, aldi_product, price, price_per_unit):
        return {
            'brand': "Aldi",
            'catagory': product,
            'product': aldi_product,
            'price': price,
            'price_per_unit': price_per_unit
        }

    def search_product(self, product, is_csv=True):
        """
        Searches for product.
        product = Name of grocery we want.
        is_csv: True, as when I run locally, I want to see it in terminal.
        """

        query = json.dumps({"Query": product})
        url = "https://groceries.aldi.ie/api/aldisearch/autocomplete"
        response = requests.post(url=url, headers=self._headers, params=self._params, data=query)

        resp = {
            'products': [],
            'meta': []
        }
        for item in response.json()['Suggestions']:

            aldi_product = standardise(item['DisplayName'])
            # Aldi actually rename too many things, this isn't really possible to do
            for ownbrand in ['clonbawn', "healys farm",
                             "ballymore crust",
                             "healys",
                             "egans", "kavanaghs",
                             "harvest morn", "natures pick"]:
                if ownbrand in aldi_product:
                    aldi_product = replace_ownbrand(aldi_product, ownbrand)

            price = float(item['ListPrice'])
            price_per_unit = float(item['UnitPrice'])
            if is_csv:
                resp['products'].append(self.format_dict(product, aldi_product, price, price_per_unit))
                resp['meta'].append(price)
            else:
                generate_insert(product, aldi_product, 'aldi', price, f"https://groceries.aldi.ie{item['Url']}")

        return resp
