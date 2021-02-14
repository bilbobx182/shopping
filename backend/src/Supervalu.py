from backend.src.common import replace_ownbrand,remove_currency,generate_insert,perform_request

class Supervalu():

    def __init__(self,catagories):
        self._catagories = catagories

    def get_supervalu_products(self):
        for catagory in self._catagories:
            return_list = []
            soup = perform_request(f'https://shop.supervalu.ie/shopping/search/allaisles?q={catagory}')
            for product in soup.find_all("div", {"id": "search-all-aisles-listings-view"})[0].contents:
                try:
                    if "LISTING-MID-0" not in product.text:
                        data = remove_currency(replace_ownbrand(
                            product.text.split("\n\n\n\n\n\n\n")[3].replace("\n", "").replace("                ",
                                                                                              "").strip(),
                            "supervalu")).split("    ")
                        item = (data[0])
                        url = product.find_all('a')[0].attrs['href']
                        sql = generate_insert(catagory, item, 'SuperValu', data,url)
                        return_list.append(sql)
                except AttributeError as e:
                    continue
                except IndexError as e:
                    continue
            return return_list