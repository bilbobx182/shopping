import pandas as pd
import numpy as np
from statistics import median, mode

class Ranks:

    df = None
    median_prices = None

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

        median_prices = self.df.groupby(['company', 'category'])['price'].median().reset_index()

        # Rank the companies within each category based on their median prices
        median_prices['score'] = median_prices.groupby('category')['price'].rank(method='min')
        self.median_prices = median_prices
        self.rank_data()

    def rank_data(self):
        if self.median_prices is None:
            return None

        # Scale the ranks to 1-4, with 1 being the lowest median price and 4 being the highest median price
        max_rank = self.median_prices['score'].max()
        self.median_prices['score'] = max_rank - self.median_prices['score'] + 1

        return self.median_prices.to_dict(orient='records')



    def total_score(self, product):

        if self.median_prices is None:
            return None
        category_scores = self.median_prices.groupby('company')['score'].sum()
        # Find the category with the highest total score
        max_score_category = category_scores.idxmax()
        print(f"Best shop for {product} is {max_score_category}")
        print(f"Aldi,{category_scores['Aldi']}, Tesco,{category_scores['Tesco']},Supervalu,{category_scores['SuperValu']},Dunnes,{category_scores['dunnes']} ")

