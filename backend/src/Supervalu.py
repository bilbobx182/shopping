from common import replace_ownbrand, standardise, \
    generate_insert, replace_if, remove_string_from_number

from FoodModel import Food
import requests
import random

class Supervalu():

    def remove_garbage(self, raw_product):

        unit_price = raw_product.split("product description")[1].split("€")[2].split("/")[0]

        raw_product = raw_product.split("a Day")[0].replace(",", "").split("€")
        super_product = raw_product[0]
        super_product = replace_ownbrand(standardise(super_product), "supervalu")
        super_product = replace_if(super_product, ['signature tastes'])

        try:
            raw_price = raw_product[2].split(" ")[0]
            if "/" in raw_price:
                price = float(raw_price.split("/")[0])
            else:
                price = float(raw_price)

        except:
            price = float(raw_product[3].split(" ")[0])

        return [super_product.rstrip(), price, unit_price]

    def format_dict(self, product, item):

        try:
            unit = item['pricePerUnit'].replace("€","").split("/")[0]
        except KeyError:
            unit = item['priceNumeric']
        return {
            'company': "SuperValu",
            'category': product,
            'product': item['description'],
            'price': item['priceNumeric'],
            'unit_price': unit ,
            'url': f"https://shop.supervalu.ie/sm/delivery/rsid/5550/product/{item['description']}"
        }

    def perform_request(self,product,super_data,page=1):
        """
        Recursive pagination of the data
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'X-Correlation-Id': '74d9050e-dc94-429d-9719-1716e71f6659',
            'X-Site-Host': 'https://shop.supervalu.ie',
            'X-Shopping-Mode': '22222222-2222-2222-2222-222222222222',
            'x-customer-session-id': 'https://shop.supervalu.ie|50aa0b41-e513-47fd-a320-56bcf9e876dc',
            'X-Site-Location': 'HeadersBuilderInterceptor',
            'Origin': 'https://shop.supervalu.ie',
            'Connection': 'keep-alive',
            'Referer': 'https://shop.supervalu.ie/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }
        params = {
            'q': product,
            'take': '30',
            'skip': '30',
            'page': page,
        }

        resp = requests.get('https://storefrontgateway.supervalu.ie/api/stores/5550/search', params=params,
                                headers=headers).json()

        super_data.extend(resp['items'])
        if len(super_data) <= resp['total']:
            self.perform_request(product, super_data, page+1)

        return super_data
    def search_product(self, product):
        """
        Searches for product.
        product = Name of grocery we want.
        is_csv: True, as when I run locally, I want to see it in terminal.
        """
        resp = []

        for item in self.perform_request(product,[]):
            try:
                resp.append(Food(**self.format_dict(product,item)))
            except AttributeError as e:
                continue
            except IndexError as e:
                continue
        return resp
