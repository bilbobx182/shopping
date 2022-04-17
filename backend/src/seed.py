from Tesco import Tesco
from Supervalu import Supervalu
from database import DBConnector
from Aldi import Aldi

# CREATE TABLE product (
#       id serial PRIMARY KEY,
#       catagory  VARCHAR NOT NULL,
#       description VARCHAR  NOT NULL,
#       retailer VARCHAR  NOT NULL,
#       price FLOAT NOT NULL,
#       last_updated TIMESTAMP NOT NULL ,
#       brand VARCHAR NOT NULL,
#       sku VARCHAR NOT NULL,
#       url VARCHAR NOT NULL,
#       other VARCHAR
#   );

catagories = ["Milk chocolate digestives",
              "milk",
              "butter",
              "carrots",
              "parsnip",
              "Raspberries",
              "bananas",
              "wine",
              "porridge",
              "cereal",
              "mandarins",
              "Mushrooms",
              "Broccoli",
              "Potato",
              "Apple",
              "Orange",
              "Cabbage",
              "beans",
              "Cucumber",
              "Celery",
              "Pear",
              "Eggs",
              "Blueberry",
              "Spinach",
              "beetroot",
              "garlic",
              "pepper",
              "olive oil",
              "tofu",
              "vinegar",
              "lemon",
              "lime",
              "onion",
              "Kale",
              "Grape",
              "Pepper",
              "Tomato",
              "avocado",
              "noodles",
              "bread",
              "Dog food",
              "Granulated sugar",
              "Cola",
              "Fanta",
              "Lemonade",
              "Crisps",
              "Nuts",
              "Nachos",
              "Coca-Cola",
              "Cadbury",
              "Avonmore",
              "Brennans",
              "Lucozade",
              "Tayto",
              "7 up",
              "Jacobs",
              "Goodfellas",
              "Monster",
              "Nescafe",
              "Red Bull",
              "Pringles",
              "Ballygowan",
              "Dairygold",
              "Kinder",
              "Yoplait",
              "McVities",
              "Pat The Baker",
              "Club",
              "chickpea",
              "pasta"]

db = DBConnector()

tesco = Tesco(catagories)
sql = tesco.get_tesco_products()
db.perform_insert(sql)

sv = Supervalu(catagories)
sql = sv.get_supervalu_products()
db.perform_insert(sql)

aldi = Aldi(catagories)
sql = aldi.get_aldi_products()
db.perform_insert(sql)
