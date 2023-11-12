from common import perform_request_with_agent, standardise, replace_ownbrand, \
    reg_replace, remove_string_from_number, remove_currency, replace_if, round_up

from constants import TESCO
from FoodModel import Food


def format_dict(product, cleaned, url):
    """
    Format dictionary so it can then be used in a model.
    """
    return {
        'company': TESCO,
        'category': product,
        'product': cleaned[0],
        'price': round_up(cleaned[1]),
        'unit_price': round_up(cleaned[2]),
        'url': url,
    }


class Tesco:
    """
    Class for Teco
    """

    def remove_garbage(self, raw_html):
        """
        Method to parse the tesco HTML text and make it useable data.
        """
        if "toggle" in raw_html:
            return None

        if "any" in raw_html:
            return None

        if "out of stock" in raw_html:
            return None

        if "meal deal" in raw_html:
            # Don't want to deal with this ignore for now
            return None

        raw_html = replace_if(raw_html, ["write a review", "aldi price match"])

        known_reg = [
            {"start": "quantity", "end": "add"},
            {"start": "rest", "end": "shelf"},
            {"start": "clubcard", "end": "2023"},
            {"start": "until", "end": "2023"}
        ]

        for remove in known_reg:
            if remove['start'] and remove['end'] in raw_html:
                raw_html = reg_replace(remove['start'], remove['end'], raw_html)

        product_info = raw_html.split("€")
        product_info[0] = standardise(replace_ownbrand(product_info[0], TESCO.lower()))
        product_info[1] = float(remove_string_from_number(remove_currency(product_info[1])))
        product_info[2] = float(product_info[2].split("/")[0])
        # [product, price , price per kg]
        return product_info

    def search_product(self, product):
        """
        Searches for product.
        product = Name of grocery we want.
        is_csv: True, as when I run locally, I want to see it in terminal.
        """
        resp = []

        params = {
            'query': product,
            'icid': 'tescohp_sws-1_m-sug_in-cola_out-cola',
        }
        soup = perform_request_with_agent('https://www.tesco.ie/groceries/en-IE/search', params)
        for row in soup.find_all("li", {"class": "product-list--list-item"}):
            raw_html = row.next_element.next_element.text.lower()

            url = f"https://www.tesco.ie/{row.find_all('a', href=True)[0].attrs['href']}"
            cleaned = self.remove_garbage(raw_html)
            if cleaned:
                resp.append(Food(**format_dict(product, cleaned, url)))

        return resp
