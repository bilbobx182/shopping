from common import perform_request_tesco, standardise, replace_ownbrand, reg_replace


class Tesco():
    """
    Class for Teco
    """

    def remove_garbage(self, raw_html):
        """
        Method to parse the tesco HTML text and make it useable data.
        """

        known_str = ["write a review", "aldi price match"]
        for remove in known_str:
            if remove in raw_html:
                raw_html = raw_html.replace(remove, "")

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
        product_info.append("tesco")
        # [product, price , price per kg, tesco]
        return product_info

    def search_product(self, product):
        """
        Product : String of the item you want from the shops.
        """
        params = {
            'query': product,
            'icid': 'tescohp_sws-1_m-sug_in-cola_out-cola',
        }
        soup = perform_request_tesco('https://www.tesco.ie/groceries/en-IE/search', params)
        for row in soup.find_all("li", {"class": "product-list--list-item"}):
            raw_html = row.next_element.next_element.text.lower()
            self.remove_garbage(raw_html)
