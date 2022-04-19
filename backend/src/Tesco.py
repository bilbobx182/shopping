from common import perform_request, generate_insert
import re


class Tesco():

    def get_brand(self, product_information):
        return str(
            product_information[0].split("SAVE")[0] if 'save' in product_information else {product_information[0]})

    def remove_suggestions(self, brand):
        return str(brand.split("Cheaper")[0] if "Cheaper alternatives" in brand else brand)

    def remove_after_keyword(self, brand, search):
        return str(brand.split(search)[0] if search in brand else brand)

    def reg_replace(self, start, end, data):
        """
        Method to replace substring between two start strings.
        :param start: starting string ie hello
        :param end: terminating string ie world
        :param data: hello to another world this is ciaran.
        :return: the string with everything gone between start and end : this is ciaran
        """
        reg = "(%s).*?(%s)" % (start, end)
        r = re.compile(reg, re.DOTALL)
        return r.sub('', data)

    def format_data(self, data):
        data = data.lower().replace("\n", "").replace("tesco", "ownbrand")
        # TODO Tesco is _really_ painful to scrape. 100% there's a better way to do this.
        # Clean this up in the future. I did this just to get it working, not working nicely.
        if "was" not in data:
            if "delivery" not in data:
                if ("review" in data):
                    data = self.reg_replace('write', 'shelf', data)
                if "save" in data:
                    data = self.reg_replace('save', 'now', self.reg_replace('offer', 'shelf', data))
                if ("price match" in data):
                    # Otherwise we have a long string with tesco repeating stuff
                    product_info = data.replace("aldi price match", "")
                    return product_info.split("€")[:2]
                return data.split("€")

    def _get_brand(self, data):
        return self.remove_after_keyword(
            self.remove_after_keyword(self.remove_after_keyword(self.remove_suggestions
                                                                (self.get_brand(data)), "SAVE"), "Any "),
            "Buy any").replace("'", "").replace("{", "").replace("}", "").strip()

    def __init__(self, compare_items):
        self._compare_items = compare_items

    def get_tesco_products(self):
        return_list = []
        for catagory in self._compare_items:
            soup = perform_request(f"https://www.tesco.ie/groceries/en-IE/search?query={catagory}")
            for row in soup.find_all("li", {"class": "product-list--list-item"}):
                desc = row.next_element.next_element.text.lower()
                # TODO refactor this. It's really badly done just so it'd work.
                # TODO since i was trying to figure out all edge cases one by one as I found them
                # if not any(ignore_item in desc for ignore_item in list_of_ignore):
                if 'unavailable' not in desc:
                    if "selected range" not in desc:
                        if "eachany" not in desc:
                            url = f"https://www.tesco.ie{row.find_all('a')[0].attrs['href']}"
                            product_info = self.format_data(desc)
                            if product_info:
                                return_list.append(
                                    generate_insert(catagory, self._get_brand(product_info), 'Tesco', product_info,
                                                    url))

        return return_list
