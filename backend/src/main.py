from src.Tesco import Tesco
from src.Supervalu import Supervalu
from src.database import DBConnector
import json
from fastapi import FastAPI
import uvicorn

# tesco = Tesco(shopping_list)
# supervalu = Supervalu(shopping_list)
#
# tesco.get_tesco_products()
# supervalu.get_supervalu_products()
# sql = tesco.get_tesco_products() + supervalu.get_supervalu_products()
#
# for item in (sql):
#     print(item)


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/products")
def read_root():
    return {"Hello": "World"}


@app.get("/products/{item_name}")
def read_item(item_name: str):
    result = db.get_item(item=item_name)
    if (result):
        return (result)
    else:
        tesco = Tesco([item_name])
        supervalu = Supervalu([item_name])

        tesco.get_tesco_products()
        supervalu.get_supervalu_products()
        sql = tesco.get_tesco_products() + supervalu.get_supervalu_products()
        db.perform_insert(sql)

        return db.get_item(item=item_name)


if __name__ == "__main__":
    global db
    db = DBConnector()
    uvicorn.run(app, host="0.0.0.0", port=8000)