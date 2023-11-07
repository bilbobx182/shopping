from common import perform_request_tesco, standardise, replace_ownbrand,\
    reg_replace,remove_string_from_number,remove_currency, replace_if, generate_insert, price_per_unit
class Tesco():
    """
    Class for Teco
    """

    def remove_garbage(self, raw_html):
        """
        Method to parse the tesco HTML text and make it useable data.
        """
        if "toggle" in raw_html:
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
        product_info[0] = standardise(replace_ownbrand(product_info[0], "tesco"))
        product_info[1] = remove_string_from_number(remove_currency(product_info[1]))
        # [product, price , price per kg]
        return product_info


    def format_dict(self, product,cleaned,price_per_unit):
        return {
            'brand': 'Tesco',
            'catagory': product,
            'product': cleaned[0],
            'price': float(cleaned[1]),
            'price_per_unit' : 1
        }

    def search_product(self, product, is_csv=True):
        """
        Searches for product.
        product = Name of grocery we want.
        is_csv: True, as when I run locally, I want to see it in terminal.
        """
        resp = {
            'products': [],
            'meta': []
        }

        params = {
            'query': product,
            'icid': 'tescohp_sws-1_m-sug_in-cola_out-cola',
        }
        soup = perform_request_tesco('https://www.tesco.ie/groceries/en-IE/search', params)
        for row in soup.find_all("li", {"class": "product-list--list-item"}):
            raw_html = row.next_element.next_element.text.lower()
            cleaned = self.remove_garbage(raw_html)
            if cleaned:
                if is_csv:
                    unit_price = price_per_unit(cleaned,company='tesco')
                    resp['products'].append(self.format_dict(product, cleaned,unit_price))
                    resp['meta'].append(float(cleaned[1]))
                else:
                    generate_insert(product,cleaned[0],'tesco',cleaned[1], None)

        return resp