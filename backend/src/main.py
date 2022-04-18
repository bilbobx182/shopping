from Tesco import Tesco
from Supervalu import Supervalu
from Aldi import Aldi
from database import DBConnector
from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/products")
def read_root():
    return {"Hello": "World"}


def get_data(item_name:str):
    """
    Method to get data from the various store providers.

    :param item_name:
    :return: list of dicts.
    """
    tesco = Tesco([item_name])
    supervalu = Supervalu([item_name])
    aldi = Aldi([item_name])
    sql = tesco.get_tesco_products() + supervalu.get_supervalu_products() + aldi.get_aldi_products()
    db.perform_insert(sql)
    return get_result_from_db(item_name)


def get_result_from_db(item_name:str):
    result = db.get_item(item=item_name)
    return_data = []
    try:
        for item in result:
            return_data.append({'key': item[0], 'description': item[1], 'shop': item[2], 'price': item[3], 'url': item[4]})
    except Exception as e:
        print(e)
    return return_data

@app.get("/products/{item_name}")
def read_item(item_name: str):
    """
    API endpoint of reading
    :param item_name:
    :return:
    """
    is_old_data = db.is_old_data(item=item_name)
    if is_old_data:
        # Then logically get the new set of data.
        return get_data(item_name)
    else:
        return get_result_from_db(item_name)


if __name__ == "__main__":
    global db
    db = DBConnector()
    uvicorn.run(app, host="0.0.0.0", port=8000)
