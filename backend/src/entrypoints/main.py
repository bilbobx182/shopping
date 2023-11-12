from stores.Tesco import Tesco
from stores.Supervalu import Supervalu
from Aldi import Aldi
from stores.Dunnes import Dunnes
from database import DBConnector
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
origins = ["*"]

# Configure the backend so requests can be sent so we don't have CORS issues.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tesco = Tesco()
supervalu = Supervalu()
aldi = Aldi()
dunnes = Dunnes()


@app.get("/")
def root():
    """
    Dummy method to ping.
    :return: Dict
    """
    return {"Version": "2.0.0"}


def get_data(item_name: str):
    """
    Method to get data from the various store providers.

    :param item_name:
    :return: list of dicts.
    """
    aldi_prod = aldi.search_product(item_name, is_csv=False)
    super_prod = supervalu.search_product(item_name, is_csv=False)
    dunnes_products = dunnes.search_product(item_name, is_csv=False)
    tesco_prod = tesco.search_product(item_name, is_csv=False)
    # Perform sequentially in case one has an issue inserting we still have some data.
    db.perform_insert(aldi_prod)
    db.perform_insert(super_prod)
    db.perform_insert(dunnes_products)
    db.perform_insert(tesco_prod)
    return get_result_from_db(item_name)


def get_result_from_db(item_name: str):
    """
    When needed we get an item from the DB.
    :param item_name:
    :return:
    """
    result = db.get_item(item=item_name)
    return_data = []
    try:
        for item in result:
            return_data.append(
                {'key': item[0], 'description': item[1], 'shop': item[2], 'price': item[3], 'url': item[4],
                 'last_updated': item[5]})
    except Exception as e:
        # TODO catch less broad exceptions.
        print(e)
    return return_data


@app.get("/products/{item_name}")
def read_item(item_name: str):
    """
    Main API endpoint for querying items.
    :param item_name:
    :return: [{items},{items}]
    """
    global db
    # reset it to nothing to avoid dying connections.
    db = ""
    db = DBConnector()
    fetch_new = db.should_fetch_new(item=item_name)
    if fetch_new:
        # Then logically get the new set of data.
        return get_data(item_name)
    else:
        return get_result_from_db(item_name)


if __name__ == "__main__":
    """
    Start the fast API with SSL.
    """
    # Todo don't hardcode this, set by env vars.
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn.run(app, host="0.0.0.0", port=8000, ssl_keyfile="/ssl/key.pem", ssl_certfile="/ssl/cert.pem")
