from datetime import date

WAIT_TIME = 10

today = date.today()

# dd/mm/YY
DATE = today.strftime("%Y-%m-%d")

GOOD = ['carrots', 'brocolli', 'parsnip', 'peas', 'soup', 'salad',
        'coriander', 'orange', 'apple', 'pear', 'onions', 'pineapple', 'pepper',
        'cucumber', 'aubergine', 'tomato', 'banana', 'grape', 'cherry', 'strawberry']
CARBS = ['potato', 'pasta', 'bread', 'baguette', 'pita', 'weetabix']
DAIRY = ['milk', 'yogurt', 'cheese', 'gouda', 'feta']
PROTEIN = ['chicken', 'salmon', 'beef', 'pork', 'sausages', 'steak', 'lamb', 'turkey', 'nuts', 'eggs', 'beans']
FATS = ['butter', 'mayo', 'olive oil', 'pate']
BAD = ['chocolate', 'crisps', 'cola', 'fanta', 'monster', 'redbull', 'muffins', 'biscuits', 'cakes']

FOOD_GROUPS = [GOOD, CARBS, DAIRY, PROTEIN, FATS, BAD]

ALDI = "Aldi"
DUNNES = "Dunnes"
TESCO = "Tesco"
SUPERVALU = "SuperValu"