def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def get_similar(data):
    # Filter the data to include only different brands
    filtered_data = [d for i, d in enumerate(data) if all(d['brand'] != other['brand'] for other in data[:i])]

    # Calculate Levenshtein distances
    similarities = []

    for i in range(len(filtered_data) - 1):
        for j in range(i + 1, len(filtered_data)):
            product1 = filtered_data[i]['product']
            product2 = filtered_data[j]['product']
            distance = levenshtein_distance(product1, product2)
            similarities.append((i, j, distance, filtered_data[i]['price'], filtered_data[j]['price']))

    # Sort similarities by price and lowest Levenshtein distance
    similarities.sort(key=lambda x: (x[3] + x[4], x[2]))

    for i, j, distance, price1, price2 in similarities:
        product1 = filtered_data[i]['product']
        product2 = filtered_data[j]['product']
        price1 = filtered_data[i]['price']
        price2 = filtered_data[j]['price']
        print(f"{filtered_data[i]['brand']},{ filtered_data[i]['catagory']}, {product1}, {price1}, {filtered_data[j]['brand']},{ filtered_data[j]['catagory']} , {product2}, {price2}, {distance}")