import requests
from bs4 import BeautifulSoup
from datetime import date
import re
today = date.today()

# dd/mm/YY
DATE = today.strftime("%Y-%m-%d")

def cleanse(data):
    return re.sub(r"[^a-zA-Z0-9]+", ' ', data).lower()

def remove_after_keyword(data, key):
    return str(data.split(key)[0] if key in data else data)

def replace_ownbrand(data,brand):
    return data.lower().replace(brand, "ownbrand")

def remove_currency(data):
    return data.replace('€',"")

def generate_insert(catagory,item,shop,data):
 return (f"INSERT into product values (DEFAULT,'{cleanse(catagory)}','{cleanse(item)}','{shop}','{(data[1].strip())}','{cleanse(data[2].strip())}','{DATE}');")

def perform_request(url):
    result = requests.get(url)
    return BeautifulSoup(result.content, "html.parser")