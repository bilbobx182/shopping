import datetime
import os
import sys
from time import sleep
from Dunnes import Dunnes
from Tesco import Tesco
from Aldi import Aldi
from Supervalu import Supervalu

from generate_ranks import Ranks
import multiprocessing

jobs = []

shops = {
    'Aldi': 0,
    'Tesco': 0,
    'SuperValu': 0,
    'dunnes': 0
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
def render_data(catagory):
    for product in catagory:
        aldi_prod = aldi.search_product(product)
        super_prod = super.search_product(product.lower())
        dunnes_products = dunnes.search_product(product)
        tesco_prod = tesco.search_product(product)
        try:
            # Convert from models, to dictionaries. Then combine the list of dicts.
            combined = [*[food.dict() for food in aldi_prod], *[food.dict() for food in dunnes_products],
                        *[food.dict() for food in tesco_prod], *[food.dict() for food in super_prod]]
            ranks = Ranks(combined)
            ranks.rank_data(product)
            prices.extend(ranks.get_prices(product))
            sleep(10)

        except Exception as e:
            print(e)


render_data(food)
#
# super.search_product('parsnip')
#
for item in prices:
    shops[item['shop']] += item['price']

print(shops)

# for product in food:
#         p = multiprocessing.Process(target=render_data, args=(product,))
#         jobs.append(p)
#         p.start()
#
# for proc in jobs:
#         proc.join()
