import datetime
import os
import sys

from Dunnes import Dunnes
from Tesco import Tesco
from Aldi import Aldi
from Supervalu import Supervalu
from common import stats,FOOD_GROUPS
import multiprocessing


dunnes = Dunnes()
tesco = Tesco()
aldi = Aldi()
super = Supervalu()

current_datetime = datetime.datetime.now()
formatted_date_time = current_datetime.strftime("%Y%m%d_%H%M%S")

# Convert the formatted date and time to a string
now = str(formatted_date_time)

STATS = os.getenv("STATS", False)
FILENAME = f"{now}_shopping.csv"

jobs = []

def render_data(catagory):
    file = open(FILENAME, 'a')
    sys.stdout = file
    for product in catagory:
        aldi_prod = aldi.search_product(product)
        super_prod = super.search_product(product)
        dunnes_products = dunnes.search_product(product)
        tesco_prod = tesco.search_product(product)
        try:
            if STATS:
                stats(dunnes_products['meta'], 'dunnes', product, now)
                stats(aldi_prod['meta'], 'aldi', product, now)
                stats(super_prod['meta'], 'supervalu', product, now)
                stats(tesco_prod['meta'], 'tesco', product, now)
            else:
                for result in [*aldi_prod['products'], *dunnes_products['products'], *tesco_prod['products'],
                               *super_prod['products']]:
                    print(f"{now},{result['brand']},{result['catagory']},{result['product']},{result['price']},{result['unit_price']}")
        except Exception as e:
            print()


if __name__ == '__main__':
    #Used for debugging.
    if False:
        for catagory in FOOD_GROUPS:
            for product in catagory:
                tescopro = dunnes.search_product(product)
                tescopro = tesco.search_product(product)
                supedr = super.search_product(product)
                aldir = aldi.search_product(product)

    else:
        for catagory in FOOD_GROUPS:
            p = multiprocessing.Process(target=render_data, args=(catagory,))
            jobs.append(p)
            p.start()

        for proc in jobs:
            proc.join()