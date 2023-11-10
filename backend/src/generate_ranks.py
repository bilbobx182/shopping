import pandas as pd
import numpy as np
from statistics import median, mode
from common import round_up

class Ranks:
    shops = ['Aldi', 'Tesco', 'SuperValu', 'dunnes']
    df = None
    median_prices = None
    raw_prices = None

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    def __init__(self, data, csv=False):
        """
        Set the data on init.
        """
        if csv:
            self.df = pd.read_csv(data)
        self.df = pd.DataFrame.from_dict(data)
        self._calculate_median()

    def _calculate_median(self):
        if self.df is None:
            return None

        self.raw_prices = None
        self.median_prices = None
        self.raw_prices = self.df.groupby(['company', 'category'])['price'].median()
        self.median_prices = self.raw_prices.reset_index()

        # Rank the companies within each category based on their median prices with 'dense' method for ties
        self.median_prices['score'] = self.median_prices.groupby('category')['price'].rank(method='dense', ascending=False)

        # Scale the ranks to 1-10
        max_rank = 10
        self.median_prices['score'] = (self.median_prices['score'] / self.median_prices.groupby('category')['score'].max()) * max_rank

    def get_prices(self, product):
        render_data = 'Prices '
        prices = []

        for shop in self.shops:
            price = float(self.raw_prices[shop].values[0])
            render_data += f"{shop},{product} ,{price},"
            prices.append({'shop': shop, "product": product, "price": price})
        print(render_data)
        return prices


    # Pandas is being a pain, let's try do this without using it later.
    
    def rank_data(self, product):
        if self.median_prices is None:
            return None

        # Scale the ranks to 1-4, with 1 being the lowest median price and 4 being the highest median price
        max_rank = self.median_prices['score'].max()
        self.median_prices['score'] = max_rank - self.median_prices['score'] + 1

        category_scores = self.median_prices.groupby('company')['score'].sum()
        # Find the category with the highest total score
        max_score_category = category_scores.idxmax()
        print(f"Best shop for {product} is {max_score_category}")
        result = 'Ranks '
        for shop in self.shops:
            result += f"{shop},{product} ,{category_scores[shop]},"
        print(result)
        return self.median_prices.to_dict(orient='records')


