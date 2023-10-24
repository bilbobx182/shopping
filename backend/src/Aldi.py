import json
from common import remove_currency, standardise, standardise_liquid, replace_ownbrand

import requests


class Aldi():
    historical = []
    products = []

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

    def search_product(self, product):

        query = json.dumps({"Query": product})
        url = "https://groceries.aldi.ie/api/aldisearch/autocomplete"
        response = requests.post(url=url, headers=self._headers, params=self._params, data=query)

        resp = []
        for item in response.json()['Suggestions']:

            aldi_product = standardise(item['DisplayName'])
            for ownbrand in ['clonbawn', "healys farm",
                             "ballymore crust",
                             "healys",
                             "egans", "kavanaghs",
                             "harvest morn", "natures pick"]:
                if ownbrand in aldi_product:
                    aldi_product = replace_ownbrand(aldi_product, ownbrand)

            resp.append({
                'brand': 'Aldi',
                'catagory': product,
                'product': aldi_product,
                'price': item['ListPrice'],
                'url': f"https://groceries.aldi.ie{item['Url']}"
            })
        return resp
