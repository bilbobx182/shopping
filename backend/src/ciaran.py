from Dunnes import Dunnes
from Tesco import Tesco
from common import perform_request_tesco

catagories = [
              "carrots",
              "parsnip",
              "porridge",
              "cereal",
              "Potato",
              "beans",
              "Eggs",
              "Blueberry",
              "garlic",
              "olive oil",
              "tofu",
              "lemon",
              "lime",
              "onion",
              "Grape",
              "Tomato",
              "bread",
              "Nuts",
              "Chocolate",
              "milk",
              "Monster",
              "Red Bull",
              "butter",
              "pasta"]

dunnes = Dunnes()
tesco = Tesco()
for product in catagories:
    dunnes.get_products(product)
    tesco.search_product(product)

