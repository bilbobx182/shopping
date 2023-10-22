from common import replace_ownbrand,cleanse,remove_currency,generate_insert,generate_historical,perform_request
from driver import Driver


class Dunnes():
    """
    The Dunnes class
    """

    def remove_if(self, product, condition):
        if condition not in product:
            return product
        product.remove(condition)
        return product

    def remove_garbage(self,dunnes_product):
        buy_index = dunnes_product.find("Buy")

        if buy_index != -1:
            # Find the index of the next newline character after "Buy"
            next_newline_index = dunnes_product.find("\n", buy_index)

            if next_newline_index != -1:
                # Strip the text between "Buy" and the next newline character
                dunnes_product = dunnes_product[:buy_index] + dunnes_product[next_newline_index + 1:]
            else:
                dunnes_product = dunnes_product
        else:
            dunnes_product = dunnes_product

        # Remove currency, replace the branding, and make list
        if "only" in dunnes_product:
            dunnes_product = dunnes_product.replace("only", "")
        dunnes_product = replace_ownbrand(remove_currency(dunnes_product.lower()), "dunnes stores").split("\n")
        # Cleanup garbage
        dunnes_product = self.remove_if(dunnes_product,"add to cart")
        dunnes_product = self.remove_if(dunnes_product, "open product description")
        dunnes_product = self.remove_if(dunnes_product, "view deal")
        return dunnes_product

    def get_products(self,product):
        self.driver = Driver()

        url = f"https://www.dunnesstoresgrocery.com/sm/delivery/rsid/258/results?q={product}"
        self.driver.handle_cookie("onetrust-accept-btn-handler", "button[@id=", url)
        results = self.driver.search("ColListing--1fk1zey bPxMbf","@class")

        for result in results:
            try:
                cleaned = self.remove_garbage(result.text)
                print(f"Dunnes, {cleaned[0]}")
            except AttributeError as e:
                continue
            except IndexError as e:
                continue
        self.driver.finish()


dunnes = Dunnes()
# dunnes.remove_garbage("'Coca-Cola Classic 1.5L, €3.10 \n Coca-Cola\n Buy 3 for €5 \n Coca-Cola Classic 1.5L \n Open product description \n €3.10 \n €2.07/l \n ADD TO CART \n View Deal \n'")
dunnes.get_products("cola")
dunnes.get_products("milk")
dunnes.get_products("party mix")