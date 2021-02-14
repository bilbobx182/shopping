from backend.src.common import perform_request, generate_insert


class Tesco():

    def get_brand(self, product_information):
        return str(product_information[0].split("SAVE")[0] if 'save' in product_information else {product_information[0]})

    def remove_suggestions(self, brand):
        return str(brand.split("Cheaper")[0] if "Cheaper alternatives" in brand else brand)

    def remove_after_keyword(self, brand, search):
        return str(brand.split(search)[0] if search in brand else brand)

    def format_data(self, data):
        return  (' '.join(data).replace("\n", "").replace("Add to basketQuantity", "")
                    .replace("Best Value for You", "").replace("                 ", ' ')
                    .replace("Delivering the freshest food to your door- Find out more >", "")
                    .replace("Tesco", "ownbrand")
                    .replace("Alcohol can only be delivered between 11am - 10pm Monday to Saturday.Alcohol can only be delivered between 1pm and 10pm on Sunday.","")
                    .replace("(", "")
                    .replace(")", "")
                    .replace("'","")
                    .strip()).split("€")

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
            soup = perform_request(f"https://www.tesco.ie/groceries/product/search/default.aspx?searchBox={catagory}")
            for row in soup.find_all("div", {"class": "productLists"})[0].contents[0].contents:
                split = row.text.replace("\'","").split("\r")
                split.pop(1)
                data = self.format_data(split)

                url = f"https://www.tesco.ie{row.find_all('a')[0].attrs['href']}"
                if 'not available' not in data[2] and 'Rest of Sandwiches shelf' not in data[2]:
                    brand = self._get_brand(data)
                    if ('valid from') not in brand and "Lunch Meal Deal" not in brand:
                        return_list.append(generate_insert(catagory, brand, 'Tesco', data,url))
        return return_list
