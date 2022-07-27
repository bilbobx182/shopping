import psycopg2
import datetime
from datetime import date
today = date.today()

import os

# TODO SET ENV VAR
PRICE_DAYS_BACK = 5

class DBConnector:

    def __init__(self):
        self._conn_string = f"host='con-test.cygcjduv9tkp.eu-west-1.rds.amazonaws.com' dbname='shopping' user='postgres' password='{PASSWORD}'"
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
            select = f"select id,description,retailer,price,url,last_updated from product where catagory like '{item.lower()}' order by price ASC limit (160);"
            self._cursor.execute(select)
            return self._cursor.fetchall()
        except Exception as e:
            print(e)

    def get_old(self):
        select = f"select date_trunc('hour', last_updated),id,url, from product order by date_trunc('hour', last_updated) desc limit(1);"
        self._cursor.execute(select)
        return self._cursor.fetchall()

    def should_fetch_new(self, item):
        """
        If this returns things, that means there are entries for that item within the past N days.
        Therefore we don't need to get it again
        :param item:
        :return:
        """
        select = f"select date_trunc('hour', last_updated),catagory from product WHERE date_trunc('hour', last_updated) >  NOW() - INTERVAL '{PRICE_DAYS_BACK} days' AND catagory ilike '{item}' limit(1);"
        self._cursor.execute(select)
        data = self._cursor.fetchall()

        # If there is no data returned by the cursor, that means we need to get some
        if data:
            return False
        return True
