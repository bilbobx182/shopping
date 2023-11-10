import pandas as pd
import numpy as np
from statistics import median, mode

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('20231107_165549_shopping.csv')
# Configure Pandas to display all rows and columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Calculate the median price for each category for each company
median_prices = df.groupby(['company', 'catergory'])['price'].median().reset_index()

# Rank the companies within each category based on their median prices
median_prices['score'] = median_prices.groupby('catergory')['price'].rank(method='min')

# Scale the ranks to 1-4, with 1 being the lowest median price and 4 being the highest median price
max_rank = median_prices['score'].max()
median_prices['score'] = max_rank - median_prices['score'] + 1

# Convert the ranked results to a dictionary
ranked_results_dict = median_prices.to_dict(orient='records')

# Display  the ranked results as a dictionary
print("Ranked Results as a Dictionary:")
for result in ranked_results_dict:
    print(result)

# Calculate the total score for each category
category_scores = median_prices.groupby('company')['score'].sum()

# Find the category with the highest total score
max_score_category = category_scores.idxmax()

# Display the category with the highest total score
print("Category with the Highest Total Score:", max_score_category)