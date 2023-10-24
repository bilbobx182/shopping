from Dunnes import Dunnes
from Tesco import Tesco
from Aldi import Aldi
from common import perform_request_tesco
from ai_magic import get_similar
# catagories = [
              # "porridge",
              # "cereal",
              # "Potato",
              # "beans",
               # "Milk",
              # "Eggs",
              # "Blueberry",
              # "garlic",
              # "olive oil",
              # "tofu",
              # "lemon",
              # "lime",
              # "onion",
              # "Grape",
              # "Tomato",
              # "bread",
              # "Nuts",
              # "Chocolate",
              # "milk",
              # "Monster",
              # "Red Bull",
              # "butter",
              # "pasta"]

dunnes = Dunnes()
tesco = Tesco()
aldi = Aldi()
for product in ["Tomato"]:
    res = aldi.search_product(product)
    print(res)
    # dunnes_products = dunnes.search_product(product)
    # tesco_products = tesco.search_product(product)
    # combined = [*dunnes_products, *tesco_products]
    # get_similar(combined)
