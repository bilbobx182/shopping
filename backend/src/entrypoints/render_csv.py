import os
import sys

from stores.Dunnes import Dunnes
from stores.Tesco import Tesco
from stores.Aldi import Aldi
from stores.Supervalu import Supervalu
from constants import FOOD_GROUPS, DATE
from generate_ranks import get_price_stats, averages

dunnes = Dunnes()
tesco = Tesco()
aldi = Aldi()
super = Supervalu()

shop_objs = [aldi, tesco, dunnes, super]

STATS = os.getenv("STATS", False)
FILENAME = f"{DATE}_shopping.csv"

jobs = []


def render_data(product):
    file = open(FILENAME, 'a')
    sys.stdout = file

    for shop in shop_objs:
        products = shop.search_product(product)
        get_price_stats(products)


if __name__ == '__main__':

    for product in ['chocolate', 'crisps']:
        render_data(product)
