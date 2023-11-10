import datetime
import os
import sys
from time import sleep
from Dunnes import Dunnes
from Tesco import Tesco
from Aldi import Aldi
from Supervalu import Supervalu
import itertools

from generate_ranks import Ranks
import multiprocessing
from common import round_up

jobs = []

shops = {
    'Aldi': 0,
    'Tesco': 0,
    'SuperValu':  0,
    'dunnes':  0,
}

dunnes = Dunnes()
tesco = Tesco()
aldi = Aldi()
super = Supervalu()



food = ["mushroom", "Onions", "Garlic", "Tomato", "Peppers",
        "Parsnip", "Carrots", "Cheese", "Butter",
        "Milk", "Chicken", "Salmon", "Meatballs", "Tofu", "Eggs", "Turkey", "Rice", "Potato", "Bread", "Chocolate",
        "Cola"]


prices = []
def render_data(product):
    aldi_prod = aldi.search_product(product)
    super_prod = super.search_product(product)
    dunnes_products = dunnes.search_product(product)
    tesco_prod = tesco.search_product(product)
    try:
        # Convert from models, to dictionaries. Then combine the list of dicts.
        combined = [*[food.dict() for food in aldi_prod], *[food.dict() for food in dunnes_products],
                    *[food.dict() for food in tesco_prod], *[food.dict() for food in super_prod]]
        ranks = Ranks(combined)
        sleep(10)
        return ranks.get_prices()

    except Exception as e:
        print(e)


if __name__ == '__main__':

    food = ["mushroom", "cola"]

    num_processes = multiprocessing.cpu_count()
    with multiprocessing.Pool(processes=num_processes) as pool:
        prices.extend(pool.map(render_data, food))

    prices = list(itertools.chain.from_iterable(prices))
    print("Results:", prices)

    for item in prices:
        shops[item['company']] = round_up(shops[item['company']] + item['price'])


    print(shops)
