import psycopg2
import datetime

class DBConnector:

    def __init__(self):
        # TODO Fill in the password programatically at build using SED.
        # TODO set the host by an environment variable.
        self._conn_string = "host='ciarandb.cygcjduv9tkp.eu-west-1.rds.amazonaws.com' dbname='shopping' user='postgres' password='FILLMEIN'"

        self._conn = psycopg2.connect(self._conn_string)
        self._cursor = self._conn.cursor()

    def perform_insert(self, insert_data):
        """
        Method to insert the data and commit it.
        :param insert_data:
        :return:
        """
        for item in insert_data:
            print(item)
            self._cursor.execute(item)
            self._conn.commit()

    def get_item(self, item):
        select = f"select id,description,retailer,price,url from product where catagory like '{item.lower()}' order by price ASC limit (160);"
        self._cursor.execute(select)
        return self._cursor.fetchall()

    def is_old_data(self, item):
        """
        Method used for querying whether we need to refresh the data.
        :param item:
        :return:
        """
        select = f"select date_trunc('hour', last_updated),id from product  where catagory like '{item.lower()}' order by date_trunc('hour', last_updated) desc limit(1);  "
        self._cursor.execute(select)
        data = self._cursor.fetchall()
        if not data:
            # Scenario no data, therefore it's new.
            return True

        for row in data:

            if (((row[0].date() - datetime.datetime.now().date())).days > 30):
                return True
            else:
                return False
