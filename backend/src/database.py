import os
import psycopg2
from datetime import date
today = date.today()


# TODO SET ENV VAR
PRICE_DAYS_BACK = 5
DB_PASS = os.getenv("DB_PASS","pass")


class DBConnector:

    def __init__(self):
        self._conn_string = f"host='con-test.cygcjduv9tkp.eu-west-1.rds.amazonaws.com' dbname='shopping' user='postgres' password='{DB_PASS}'"
        self._conn = psycopg2.connect(self._conn_string)
        self._cursor = self._conn.cursor()

    def perform_insert(self, insert_data):
        """
        Method to insert the data and commit it.
        :param insert_data:
        :return:
        """
        try:
            for item in insert_data:
                print(item)
                self._cursor.execute(item)
                self._conn.commit()
        except Exception as e:
            print(e)

    def get_item(self, item):
        try:
            select = f"select id,description,retailer,price,url,last_updated from product where catagory like '{item.lower()}' order by last_updated ASC limit (160);"
            self._cursor.execute(select)
            return self._cursor.fetchall()
        except Exception as e:
            print(e)


    def should_fetch_new(self, item):
        """

        Checks if data has been found within the past N days.

        :param item:
        :return:
        """
        select = f"select date_trunc('hour', last_updated),catagory from product WHERE date_trunc('hour', last_updated) >  NOW() - INTERVAL '{PRICE_DAYS_BACK} days' AND catagory ilike '{item}' limit(1);"
        self._cursor.execute(select)
        data = self._cursor.fetchall()

        # If there is no data returned by the cursor, that means we need to get some
        if data:
            print(f"There is data within {PRICE_DAYS_BACK}")
            return False
        print(f"No data for {item} within past {PRICE_DAYS_BACK}")
        return True
