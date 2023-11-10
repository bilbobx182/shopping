import datetime
import os
import sys

from Dunnes import Dunnes
from Tesco import Tesco
from Aldi import Aldi
from Supervalu import Supervalu

import multiprocessing

dunnes = Dunnes()
tesco = Tesco()
aldi = Aldi()
super = Supervalu()

food = ["Mushrooms", "Onions", "Garlic", "Tomatoe", "Peppers", "Cauliflower", "Parsnip", "Carrots", "Cheese", "Butter",
        "Milk", "Chicken", "Salmon", "Meatballs", "Tofu", "Eggs", "Turkey", "Rice", "Potato", "Bread", "Chocolate",
        "Cola"]


res = aldi.search_product(food[0])
print(res)