from common import round_up
from collections import defaultdict
from statistics import median

class Ranks:
    shops = ['Aldi', 'Tesco', 'SuperValu', 'dunnes']
    df = None
    median_prices = None

    def __init__(self, data,):
        """
        Set the data on init.
        """

        self.median_prices = defaultdict(list)
        for entry in data:
            key = (entry['company'], entry['category'])
            self.median_prices[key].append(float(entry['price']))

        self._calculate_median()

    def _calculate_median(self):
        self.ranked_results = []
        for key, prices in self.median_prices.items():
            median_price = median(prices)
            # Scale the ranks to 1-10
            rank = 10 - (median_price / max(prices)) * 9
            self.ranked_results.append({'company': key[0], 'price':median_price, 'category': key[1], 'median': median_price, 'rank': rank})

        # Sort the results by rank
        self.ranked_results.sort(key=lambda x: x['rank'], reverse=True)

        return self.ranked_results

    def get_prices(self):
        for result in self.ranked_results:
            print(f"{result['company']}, {result['category']},{round_up(result['price'])},{round_up(result['rank'])}")
        return self.ranked_results
