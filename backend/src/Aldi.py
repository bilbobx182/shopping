import json
from common import standardise, replace_ownbrand, round_up
from constants import ALDI
from FoodModel import Food

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

    _own_brands = ['clonbawn', "healys farm",
                   "ballymore crust",
                   "healys",
                   "egans", "kavanaghs",
                   "harvest morn", "natures pick"]

    _params = (
        ('limit', '200'),
    )

    def remove_ownbrand(self, aldi_product):
        # Aldi actually rename too many things, this isn't really possible to do
        for ownbrand in self._own_brands:
            if ownbrand in aldi_product:
                aldi_product = replace_ownbrand(aldi_product, ownbrand)
        return aldi_product

    def search_product(self, product):
        """
        Searches for product.
        product = Name of grocery we want.
        is_csv: True, as when I run locally, I want to see it in terminal.
        """

        query = json.dumps({"Query": product})
        url = "https://groceries.aldi.ie/api/aldisearch/autocomplete"
        response = requests.post(url=url, headers=self._headers, params=self._params, data=query)

        resp = []

        for item in response.json()['Suggestions']:
            aldi_product = standardise(item['DisplayName'])
            aldi_product = self.remove_ownbrand(aldi_product)

            price = float(item['ListPrice'])
            price_per_unit = float(item['UnitPrice'].replace("€", ""))
            data = {
                "company": ALDI,
                "category": product,
                "product": aldi_product,
                "price": round_up(price),
                "unit_price": round_up(price_per_unit),
                "url": f"https://groceries.aldi.ie{item['Url']}",
            }
            resp.append(Food(**data))
        return resp
