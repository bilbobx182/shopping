import requests
import random
from bs4 import BeautifulSoup
import re
from statistics import median, mode, mean
import math




def split_at_letters(data):
    match = re.search(r'[a-zA-Z]', data)
    if match:
        split_index = match.start()
        return data[:split_index]


def reg_replace(start, end, data):
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


def replace_if(data, conditions):
    """
    Not all of the returned data has the same values.
    Therefore we need to check if it's there then delete.
    """

    for remove in conditions:
        if remove in data:
            data = data.replace(remove, "")
    return data


def remove_string_from_number(data):
    match = re.search(r'\d+\.\d+', data)

    if match:
        number_as_float = float(match.group(0))
        return number_as_float


def cleanse(data):
    return re.sub(r"[^a-zA-Z0-9]+", ' ', data).lower()


def remove_alpha(product):
    result = re.sub(r'[a-zA-Z]', "", product)
    result = re.sub(r'[^0-9.]', ' ', result)
    result = re.sub(r'\.+', '.', result)
    return result.strip().split(" ")


def remove_after_keyword(data, key):
    return str(data.split(key)[0] if key in data else data)


def replace_ownbrand(data, brand):
    return data.lower().replace(brand, "ownbrand")


def round_up(number):
    return math.ceil(number * 100) / 100

def remove_currency(data):
    return data.replace('€', "")


def generate_insert(catagory, item, shop, data, url, brand=None, sku=None):
    print(data)
    price = f"{(data[1].strip())}"
    other = f"{cleanse(data[2].strip())}" if len(data) > 3 else ''
    if (brand == None):
        brand = 'N/A'
    if (sku == None):
        sku = 'N/A'

    # Whenever we get new data with the same URL, we update the price
    rstr = f"INSERT into product values (DEFAULT,'{cleanse(catagory)}','{cleanse(item)}','{shop}','{price}','{DATE}','{brand}','{sku}','{url}','{other}') on conflict(url) do update set price = {price};"

    return rstr


def standardise(data):
    data = data.replace("'", "")

    data = remove_currency(cleanse(data))
    # Remove countries we want standardised data
    return replace_if(data, ["irish"])


def generate_historical(data, url):
    price = f"{(data[1].strip())}"
    rstr = f"INSERT into historical_prices values (DEFAULT,'{url}','{price}','{DATE}');"
    return rstr


def stats(data, brand, catagory, now):
    """
    Method used by render_csv to display the data to terminal.
    """
    print(f"{brand},{now}, {catagory},{len(data)} , {mean(data)}, {median(data)} ,{mode(data)}")


def perform_request(url):
    resp = requests.get(url=url)
    return BeautifulSoup(resp.content, "html.parser")


def perform_request_tesco(url, param):
    # For now, seperate, we can fixup later
    agent = f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/{random.randint(5, 500)}.{random.randint(5, 100)} (KHTML, like Gecko) Chrome/{random.randint(100, 120)}.0.{random.randint(5, 5000)}.{random.randint(100, 120)} Safari/{random.randint(100, 520)}.{random.randint(1, 120)}"

    head = {
        'User-Agent': agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    result = requests.get(url=url, headers=head, params=param)
    return BeautifulSoup(result.content, "html.parser")
