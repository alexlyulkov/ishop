sql_types = {'int':'INTEGER', 'long':'INTEGER', 'str':'TEXT', 'unicode':'TEXT', 'float':'REAL'}

from classes import Product, Ad, Category, Image
import psycopg2
import traceback

class database_sql():
    def __init__(self):
        self.db = None
        self.cursor = None
        self.f = None
        
    def init_postgresql(self, database, user, password, host, port):
        self.f = '%s'
        self.db = psycopg2.connect(database = database, user = user, password = password,
                                   host = host, port = port, async = 0)
        self.init_tables()
        
    def init_tables(self):
        self.cursor = self.db.cursor()
       
    def save_product(self, product):
        pass
        
    def load_product(self, product_id):
        return Product()

    def delete_product(self, product_id):
        pass

    def add_category(self, category):
        pass

    def load_category(self, category_id):
        #returns list of products with this category
        return (Product(), Product())

    def get_categories(self):
        return (Category(), Category())

    def get_random_products(self, number_of_products):
        return (Product() for i in xrange(number_of_products))

    def add_ad(self, ad):
        pass

    def delete_ad(self, ad_id):
        pass

    def get_all_ads(self):
        return (Ad(), Ad())

    def save_image(self, image):
        pass

    def get_image(self, image_id):
        pass

    def delete_image(self, image_id):
        pass
