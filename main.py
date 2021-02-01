import requests
from bs4 import BeautifulSoup
import re
import time
from common import replace_ownbrand,remove_currency
shopping = ['Cheese','Milk','Lettuce','Tomato','Bread','Garlic','Onion','Rice','Carrot']


for item in shopping:
    return_list = []
    url = f'https://shop.supervalu.ie/shopping/search/allaisles?q={item}'
    result = requests.get(url)
    soup = BeautifulSoup(result.content, "html.parser")
    for product in soup.find_all("div", {"id": "search-all-aisles-listings-view"})[0].contents:
        try:
            if "LISTING-MID-0" not in product.text:
                data = remove_currency(replace_ownbrand(product.text.split("\n\n\n\n\n\n\n")[3].replace("\n","").replace("                ","").strip(),"supervalu")).split("    ")
                brand = (data[0])
                insert = (f'INSERT into product values ({item},{brand},{data[1].strip()},{data[2].strip()});')
                print(insert)
        except AttributeError as e:
            continue
        except IndexError as e:
            continue