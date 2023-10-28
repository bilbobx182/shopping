import datetime
import sys

from Dunnes import Dunnes
from Tesco import Tesco
from Aldi import Aldi
from Supervalu import Supervalu
from common import stats


good = ['carrots', 'brocolli', 'parsnip', 'peas', 'soup', 'salad',
        'coriander', 'orange', 'apple', 'pear', 'onions', 'pineapple', 'pepper',
        'cucumber', 'aubergine', 'tomato', 'banana', 'grape', 'cherry', 'strawberry']

carbs = ['potato', 'pasta', 'bread', 'baguette', 'pita', 'weetabix']

dairy = ['milk', 'yogurt', 'cheese', 'gouda', 'feta']

protein = ['chicken', 'salmon', 'beef', 'pork', 'sausages', 'steak', 'lamb', 'turkey', 'nuts', 'eggs', 'beans']
fats = ['butter', 'mayo', 'olive oil', 'pate']

bad = ['chocolate', 'crisps', 'cola', 'fanta', 'monster', 'redbull', 'muffins', 'biscuits', 'cakes']

groups = [good, carbs, dairy, protein, fats, bad]

dunnes = Dunnes()
tesco = Tesco()
aldi = Aldi()
super = Supervalu()


current_datetime = datetime.datetime.now()
formatted_date_time = current_datetime.strftime("%Y%m%d_%H%M%S")

# Convert the formatted date and time to a string
now = str(formatted_date_time)


FILENAME = f"{now}_shopping.csv"
with open(FILENAME, 'w') as sys.stdout:
    print(f"Company, category, sampleSize ,mean, median , mode")
    for catagory in groups:
        for product in catagory:
            aldi_prod = aldi.search_product(product)
            super_prod = super.search_product(product)
            dunnes_products = dunnes.search_product(product)
            tesco_prod = tesco.search_product(product)
            try:
                stats(dunnes_products['meta'],'dunnes',product)
                stats(aldi_prod['meta'],'aldi',product)
                stats(super_prod['meta'],'supervalu',product)
                stats(tesco_prod['meta'],'tesco',product)
            except Exception as e:
                print()