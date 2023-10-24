from common import replace_ownbrand, perform_request, standardise, remove_currency, replace_if, split_at_letters


class Supervalu():

    def remove_garbage(self, raw_product):
        raw_product = raw_product.split("a Day")[0].split(",")
        super_product = replace_ownbrand(standardise(raw_product[0]), "supervalu")
        super_product = replace_if(super_product, ['signature tastes'])
        price = remove_currency(split_at_letters(raw_product[1]))
        return [super_product, float(price)]


    def search_product(self,product):
        result = []
        soup = perform_request(f'https://shop.supervalu.ie/sm/delivery/rsid/5550/results?q={product}')

        for product in soup.find_all("div", {"class": "ColListing--1fk1zey iowyBD"}):
            try:
                cleaned = self.remove_garbage(product.text)
                result.append({
                    'brand': "SuperValu",
                    'catagory': product,
                    'product': cleaned[0],
                    'price': cleaned[1]
                })
            except AttributeError as e:
                continue
            except IndexError as e:
                continue
        return result