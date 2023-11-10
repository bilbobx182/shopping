import datetime
import os
import sys

from Dunnes import Dunnes
from Tesco import Tesco
from Aldi import Aldi
from Supervalu import Supervalu

from generate_ranks import Ranks
import multiprocessing

jobs = []
dunnes = Dunnes()
tesco = Tesco()
aldi = Aldi()
super = Supervalu()

food = ["mushroom", "Onions", "Garlic", "Tomato", "Peppers", "Cauliflower",
        "Parsnip", "Carrots", "Cheese", "Butter",
        "Milk", "Chicken", "Salmon", "Meatballs", "Tofu", "Eggs", "Turkey", "Rice", "Potato", "Bread", "Chocolate",
        "Cola"]


def render_data(catagory):
    for product in catagory:
        aldi_prod = aldi.search_product(product)
        super_prod = super.search_product(product)
        dunnes_products = dunnes.search_product(product)
        tesco_prod = tesco.search_product(product)
        try:
            # Convert from models, to dictionaries. Then combine the list of dicts.
            combined = [*[food.dict() for food in aldi_prod], *[food.dict() for food in dunnes_products],
                        *[food.dict() for food in tesco_prod], *[food.dict() for food in super_prod]]
            ranks = Ranks(combined)
            ranks.total_score(product)


        except Exception as e:
            print(e)


render_data(['cola', 'onions'])

# for product in food:
#         p = multiprocessing.Process(target=render_data, args=(product,))
#         jobs.append(p)
#         p.start()
#
# for proc in jobs:
#         proc.join()
