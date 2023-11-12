from common import round_up
from constants import ALDI, SUPERVALU, TESCO, DUNNES
from collections import defaultdict
from statistics import median, mode, mean


def get_price_stats(products):
    for product in products:
        print(f"{product.company}, {product.category},{product.product}, {round_up(product.price)},{round_up(product.unit_price)}")
    averages(products)


def averages(products):
    """
    A method to render the averages for a given list of expected keys.
    """

    result = {}


    unit_prices = [item.unit_price for item in products]
    prices = [item.price for item in products]
    result.update({f'mean_unit': mean(unit_prices), f'mode_unit': mode(unit_prices), f'median_unit': median(unit_prices)})
    result.update({f'mean_price': mean(prices), f'mode_price': mode(prices), f'median_price': median(prices)})

    print(f"mean_unit, {mean(unit_prices)}, mode_unit, {mode(unit_prices)}, median_unit {median(unit_prices)}")
    print(f"mean_price, {mean(prices)}, mode_price, {mode(prices)}, median_price {median(prices)}")

    return result

class Ranks:
    shops = [ALDI, TESCO, SUPERVALU, DUNNES]
    median_prices = None

    def __init__(self, data):
        """
        Set the data on init.
        """

        self.prices = defaultdict(list)
        for entry in data:
            key = (entry['company'], entry['category'])
            self.prices[key].append(float(entry['price']))
        self._calculate_median()

    def _calculate_median(self):
        self.ranked_results = []

        for key, prices in self.prices.items():
            median_price = median(prices)
            mode_price = mode(prices)
            mean_price = mean(prices)
            # Scale the ranks to 1-10
            rank = 10 - (median_price / max(prices)) * 9
            self.ranked_results.append(
                {'company': key[0],
                 'price': median_price,
                 'category': key[1],
                 'median': median_price,
                 'mean': mean_price,
                 'mode': mode_price,
                 'rank': rank})

        # Sort the results by rank
        self.ranked_results.sort(key=lambda x: x['rank'], reverse=True)

        return self.ranked_results

    def get_prices(self):
        for result in self.ranked_results:
            print(f"{result['company']}, {result['category']},{round_up(result['price'])},{round_up(result['rank'])}")
        return self.ranked_results
