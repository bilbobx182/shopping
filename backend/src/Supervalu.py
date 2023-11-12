from common import standardise, remove_string_from_number, replace_ownbrand, round_up

from constants import SUPERVALU
from FoodModel import Food
import requests


def format_dict(product, item):

    try:
        if "€" in item['pricePerUnit']:
            unit = remove_string_from_number(item['pricePerUnit'].replace("€", "").split("/")[0])
        else:
            unit = remove_string_from_number(item['pricePerUnit'])
    except KeyError:
        # Some items don't have unit prices
        unit = item['priceNumeric']
    except Exception as e:
        unit = item['priceNumeric']

    clean = standardise(item['name'])
    return {
        'company': SUPERVALU,
        'category': product,
        'product': replace_ownbrand(clean, SUPERVALU.lower()),
        'price': round_up(item['priceNumeric']),
        'unit_price': round_up(unit),
        'url': f"https://shop.supervalu.ie/sm/delivery/rsid/5550/product/{item['name']}"
    }


class Supervalu():

    def perform_preview_request(self, product):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'X-Correlation-Id': '7cbfa93e-5914-4865-ab23-3e8781633ffe',
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
        }

        params = {
            'q': product,
            'take': '30',
        }

        response = requests.get('https://storefrontgateway.supervalu.ie/api/stores/5550/preview', params=params,
                                headers=headers)
        resp = response.json()
        return resp['products']

    def perform_request(self, product, super_data, page=1, count=0, endpoint="/api/stores/5550/search"):
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

        resp = requests.get(f'https://storefrontgateway.supervalu.ie{endpoint}', params=params,
                            headers=headers)

        # Something bad happened, abort with the data we have.
        if resp.status_code > 299:
            return super_data

        resp = resp.json()
        resp_count = count + resp['count']

        if len(resp['items']) < 1:
            # Supervalu API isn't smart. Sometimes breaks and only returns 3.
            super_data.extend(self.perform_preview_request(product))
            return super_data

        super_data.extend(resp['items'])

        try:
            if resp_count >= resp['total']:
                return super_data
        except KeyError:
            return super_data

        # Recurse otherwise
        self.perform_request(product, super_data, page + 1, resp_count)

        return super_data

    def search_product(self, product):
        """
        Searches for product.
        product = Name of grocery we want.
        is_csv: True, as when I run locally, I want to see it in terminal.
        """
        resp = []
        for item in self.perform_request(product, []):
            try:
                resp.append(Food(**format_dict(product, item)))
            except AttributeError as e:
                continue
            except IndexError as e:
                continue
        return resp
