
# TODO use the below, to automatically compare the most common entities.
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

def render_similarities(similarities,data):
    # Sort the similarities by distance
    similarities.sort(key=lambda x: x[1])

    for i, (index_pair, distance) in enumerate(similarities[:3]):
        i, j = index_pair
        # print(f"{i} and {j} with Levenshtein Distance: {distance}")
        # print(data[i])
        # print(data[j])
        if data[i]['price'] < data[j]['price']:
            print(f'Cheaper! {data[i]}')
        if data[j]['price'] < data[i]['price']:
            print(f'Cheaper! {data[j]}')
        if data[j]['price'] == data[i]['price']:
            print(f'Same! {data[i]}, {data[j]}')



def get_similar(data):
    similarities = []
    for i in range(len(data) - 1):
        for j in range(i + 1, len(data)):
            if data[i]['brand'] != data[j]['brand']:
                product1 = data[i]['product']
                product2 = data[j]['product']
                distance = levenshtein_distance(product1, product2)
                similarities.append(((i, j), distance))
    render_similarities(similarities,data)