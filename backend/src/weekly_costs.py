import multiprocessing
import itertools
import random
from time import sleep

from Dunnes import Dunnes
from Tesco import Tesco
from Aldi import Aldi
from Supervalu import Supervalu
from constants import WAIT_TIME, SUPERVALU, DUNNES, ALDI, TESCO
from generate_ranks import Ranks
from common import round_up

shops = {
    ALDI: 0,
    TESCO: 0,
    DUNNES: 0,
    SUPERVALU: 0,
}

dunnes = Dunnes()
tesco = Tesco()
aldi = Aldi()
super = Supervalu()


def generate_weekly_costs(product):
    """
    - Queries all the shops for the product.
    - Combines data for all.
    - Generates ranks and gets the prices.
    """
    sleep(random.randint(int(WAIT_TIME / 2), WAIT_TIME))
    aldi_prod = aldi.search_product(product)
    super_prod = super.search_product(product)
    dunnes_products = dunnes.search_product(product)
    tesco_prod = tesco.search_product(product)
    try:
        # Convert from models, to dictionaries. Then combine the list of dicts.
        combined = [*[food.dict() for food in aldi_prod], *[food.dict() for food in dunnes_products],
                    *[food.dict() for food in tesco_prod], *[food.dict() for food in super_prod]]
        ranks = Ranks(combined)
        return ranks.get_prices()

    except Exception as e:
        print(e)


def main():
    prices = []
    food = ["mushroom", "Onions", "Garlic", "Tomato", "Peppers", "orange", "apple", "kiwi",
            "Parsnip", "Carrots", "Cheese", "Butter",
            "Milk", "Chicken", "Salmon", "Meatballs", "Tofu", "Eggs", "Turkey", "Rice", "Potato", "Bread", "Chocolate",
            "Cola"]

    num_processes = multiprocessing.cpu_count()
    with multiprocessing.Pool(processes=num_processes) as pool:
        prices.extend(pool.map(generate_weekly_costs, food))

    prices = list(itertools.chain.from_iterable(prices))

    for item in prices:
        shops[item['company']] = round_up(shops[item['company']] + item['price'])
    print(shops)


def debug_weekly():
    """
    Method to debug weekly costs.
    """
    debug_cost = []
    # Smaller subset of all the foods
    food = ["Rice", "Potato", "Bread", "Chocolate", "Cola", "Cheese"]

    for item in food:
        debug_cost.extend(generate_weekly_costs(item))

    debug_cost = list(itertools.chain.from_iterable(debug_cost))
    for item in debug_cost:
        shops[item['company']] = round_up(shops[item['company']] + item['price'])
    print(shops)


if __name__ == '__main__':
    debug = False
    if debug:
        # Debugging multi-process can be a pain, this makes it easier.
        debug_weekly()
    else:
        main()
