import requests
from bs4 import BeautifulSoup

def remove_after_keyword(data, key):
    return str(data.split(key)[0] if key in data else data)

def replace_ownbrand(data,brand):
    return data.lower().replace(brand, "own_brand")

def remove_currency(data):
    return data.replace('€',"")

def generate_insert(catagory,item,shop,data):
    return (f'INSERT into product values ({catagory},{item},{shop},{data[1].strip()},{data[2].strip()});')

def perform_request(url):
    result = requests.get(url)
    return BeautifulSoup(result.content, "html.parser")