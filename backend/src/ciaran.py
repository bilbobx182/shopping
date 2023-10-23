from Dunnes import Dunnes
from Tesco import Tesco
from common import perform_request_tesco

catagories = [
              "carrots",
              "parsnip",]
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
    dunnes.search_product(product)
    results = tesco.search_product(product)

