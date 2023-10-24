from Dunnes import Dunnes
from Tesco import Tesco
from common import perform_request_tesco
from ai_magic import get_similar
catagories = ["milk"]
              # "porridge",
              # "cereal",
              # "Potato",
              # "beans",
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
for product in catagories:
    dunnes_products = dunnes.search_product(product)
    tesco_products = tesco.search_product(product)
    combined = [*dunnes_products, *tesco_products]
    get_similar(combined)
