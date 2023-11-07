from common import replace_ownbrand, perform_request, standardise, \
    generate_insert, replace_if, remove_string_from_number


class Supervalu():

    def remove_garbage(self, raw_product):
        raw_product = raw_product.split("a Day")[0].replace(",", "").split("€")
        super_product = raw_product[0]
        super_product = replace_ownbrand(standardise(super_product), "supervalu")
        super_product = replace_if(super_product, ['signature tastes'])
        try:
            price = remove_string_from_number(raw_product[1])
            unit_price = float(raw_product[3].split("/")[0])
        except:
            price = remove_string_from_number(raw_product[-1:][0])
        return [super_product.rstrip(), price, unit_price]

    def format_dict(self, product, cleaned):
        return {
            'brand': "SuperValu",
            'catagory': product,
            'product': cleaned[0],
            'price': cleaned[1],
            'unit': cleaned[2],

        }

    def search_product(self, product, is_csv=True):
        """
        Searches for product.
        product = Name of grocery we want.
        is_csv: True, as when I run locally, I want to see it in terminal.
        """
        resp = {
            'products': [],
            'meta': []
        }

        soup = perform_request(f'https://shop.supervalu.ie/sm/delivery/rsid/5550/results?q={product}')

        for item in soup.find_all("div", {"class": "ColListing--1fk1zey iowyBD"}):
            try:
                cleaned = self.remove_garbage(item.text)
                if is_csv:
                    resp['products'].append(self.format_dict(product, cleaned))
                    resp['meta'].append(float(cleaned[1]))
                else:
                    generate_insert(product, cleaned[0], 'supervalue', cleaned[1], None)

            except AttributeError as e:
                continue
            except IndexError as e:
                continue
        return resp
