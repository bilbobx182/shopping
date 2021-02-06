import psycopg2


class DBConnector:

    def __init__(self):
        self._conn_string = "host='localhost' dbname='shopping' user='postgres'"
        self._conn = psycopg2.connect(self._conn_string)
        self._cursor = self._conn.cursor()

    def perform_insert(self,insert_data):
        for item in insert_data:
            print(item)
            self._cursor.execute(item)
            self._conn.commit()


    def get_item(self, item):

        select = f"select catagory,description,shop,price from product where catagory like '{item.lower()}' order by price ASC limit (20);"
        self._cursor.execute(select)
        return self._cursor.fetchall()
