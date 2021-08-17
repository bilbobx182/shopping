from backend.src.Tesco import Tesco
from backend.src.Supervalu import Supervalu
from backend.src.database import DBConnector
from fastapi import FastAPI
import uvicorn

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

        return [{'key': item[0], 'description': item[1], 'shop': item[2], 'price': item[3],'url' : item[4]} for item in result]

    else:
        tesco = Tesco([item_name])
        supervalu = Supervalu([item_name])

        tesco.get_tesco_products()
        supervalu.get_supervalu_products()
        sql = tesco.get_tesco_products() + supervalu.get_supervalu_products()
        db.perform_insert(sql)
        result = db.get_item(item=item_name)
        return [{'key': item[0], 'description': item[1], 'shop': item[2], 'price': item[3],'url' : item[4]} for item in result]


if __name__ == "__main__":
    global db
    db = DBConnector()
    uvicorn.run(app, host="0.0.0.0", port=8000)
