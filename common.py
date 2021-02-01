def remove_after_keyword(data, key):
    return str(data.split(key)[0] if key in data else data)

def replace_ownbrand(data,brand):
    return data.lower().replace(brand, "own_brand")

def remove_currency(data):
    return data.replace('€',"")