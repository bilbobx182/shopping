from common import replace_ownbrand,remove_currency,perform_request_tesco,\
    reg_replace,remove_string_from_number, standardise, replace_if


class Dunnes():
    """
    The Dunnes class
    """

    def remove_garbage(self, raw_product):
        raw_product = raw_product.split("<br/>")[0]

        raw_product = replace_if(raw_product, ["<b>Features</b>"])
        dunnes_product = reg_replace("<br/>", "Cart", raw_product)

        dunnes_product = dunnes_product.split(",")
        dunnes_product[0] = replace_ownbrand(standardise(dunnes_product[0]), "dunnes stores")
        dunnes_product[1] = remove_string_from_number(remove_currency(dunnes_product[1]))
        return dunnes_product

    def search_product(self, product):
        resp = []
        url = f"https://www.dunnesstoresgrocery.com/sm/delivery/rsid/258/results"
        soup = perform_request_tesco(url, {'q':product})
        for row in soup.find_all("div", {"class": "ColListing--1fk1zey bPxMbf"}):
            try:
                cleaned = self.remove_garbage(row.text)
                # print(f"Dunnes, {product} , {cleaned[0]}, {cleaned[1]}")
                resp.append({
                    'brand' : "Dunnes",
                    'catagory' : product,
                    'product' : cleaned[0],
                    'price' :  cleaned[1]
                })
            except AttributeError as e:
                continue
            except IndexError as e:
                continue
            finally:
                return resp