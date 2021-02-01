import requests
from bs4 import BeautifulSoup
import re
import time

class Tesco():

    def get_brand(self,product_information):
        return str(product_information[0].split("SAVE")[0] if 'save' in data else {product_information[0]})


    def remove_suggestions(self,brand):
        return str(brand.split("Cheaper")[0] if "Cheaper alternatives" in brand else brand)

    def remove_after_keyword(self,brand,search):
        return str(brand.split(search)[0] if search in brand else brand)


    def __init__(self,compare_items):
        self._compare_items = compare_items

    def get_data(self):
        return_list = []
        for item in self._compare_items:
                url = f"https://www.tesco.ie/groceries/product/search/default.aspx?searchBox={item}"
                result = requests.get(url)
                soup = BeautifulSoup(result.content, "html.parser")

                for row in soup.find_all("div", {"class": "productLists"})[0].contents[0].contents:
                        split = row.text.split("\r")
                        split.pop(1)
                        data = (' '.join(split).replace("\n","").replace("Add to basketQuantity","")
                              .replace("Best Value for You","").replace("                 ",' ')
                              .replace("Delivering the freshest food to your door- Find out more >","")
                              .replace("Tesco","Own_Brand")
                              .replace("(","")
                              .replace(")", "")
                              .strip()).split("€")


                        if 'not available' not in data[2] and 'Rest of Sandwiches shelf' not in data[2]:
                                brand = \
                                    self.remove_after_keyword(self.remove_after_keyword(self.remove_after_keyword(
                                    self.remove_suggestions(self.get_brand(data)
         ),"SAVE"),"Any "),"Buy any")

                                brand = brand.replace("'","").replace("{","").replace("}","").strip()

                                if('valid from') not in brand and "Lunch Meal Deal" not in brand:
                                    return_list.append('INSERT into product values ({item},{brand},{data[1].strip()},{data[2].strip()});')
        return return_list