sql_types = {'int':'INTEGER', 'long':'INTEGER', 'str':'TEXT', 'unicode':'TEXT', 'float':'REAL'}

from classes import Product, Ad, Category, Image
import psycopg2
import traceback
#from random import randrange

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
        try:
            columns = Category().to_dict()
            del columns['id']
            request = 'CREATE TABLE IF NOT EXISTS Category '
            request += "(id INTEGER PRIMARY KEY UNIQUE"
            for column, value in columns.items():
                request += ', ' + column + ' ' + \
                           sql_types[type(value).__name__]
            request += ")"
            self.cursor.execute(request)
            self.db.commit()


            columns = Product().to_dict()
            del columns['id']
            request = 'CREATE TABLE IF NOT EXISTS Product '
            request += "(id INTEGER PRIMARY KEY UNIQUE"
            for column, value in columns.items():
                request += ', ' + column + ' ' + \
                           sql_types[type(value).__name__]
            request += ")"
        
            self.cursor.execute(request)
            self.db.commit()



            columns = Ad().to_dict()
            del columns['id']

            request = 'CREATE TABLE IF NOT EXISTS Ad '
            request += "(id INTEGER PRIMARY KEY UNIQUE"
            for column, value in columns.items():
                request += ', ' + column + ' ' + \
                           sql_types[type(value).__name__]
            request += ")"
        
            self.cursor.execute(request)
            self.db.commit()


            columns = Image().to_dict()
            del columns['id']

            request = 'CREATE TABLE IF NOT EXISTS Image '
            request += "(id INTEGER PRIMARY KEY UNIQUE"
            for column, value in columns.items():
                request += ', ' + column + ' ' + \
                           sql_types[type(value).__name__]
            request += ")"
        
            self.cursor.execute(request)
            self.db.commit()
        except Exception as e:
            print e

    def save_product(self, product):

        parameters = product.to_dict().keys():
        request = 'UPDATE Product SET '
        for column in parameters:
            request += column + '=' + self.f + ', '
        
        request = request[0:-2]
        request += " WHERE id = " + str(product.id)
        try:
            self.cursor.execute(request, parameters.values())
            self.db.commit()
        except Exception as e:
            print e
        
    def load_product(self, product_id):

        columns = Employee().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Product '

        try:
            self.cursor.execute(request)
            rows = self.cursor.fetchall()

        except Exception as e:
            print e
            rows = []

        products = []
        for row in rows:
            values_dict = {}
            for i in xrange(len(columns)):
                values_dict[columns[i]] = row[i]
            product = Product()
            product.set_values(values_dict)
            products.append(product)
        return products


    def delete_product(self, product_id):
        try:
            self.cursor.execute("DELETE from Products where Id = %s" % product_id)
            self.db.commit
            print("Total rows deleted: %s" % self.cursor.rowcount)
        except Exception as e:
            print e

    def add_category(self, category):

        parameters = category.to_dict().keys():
        request = 'UPDATE Category SET '
        for column in parameters:
            request += column + '=' + self.f + ', '
        
        request = request[0:-2]
        request += " WHERE id = " + str(category.id)
        try:
            self.cursor.execute(request, parameters.values())
            self.db.commit()
        except Exception as e:
            print e

    def load_category(self, category_id):

        columns = Employee().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Product '
        request += ' WHERE category = '
        request += category_id

        try:
            self.cursor.execute(request)
            rows = self.cursor.fetchall()

        except Exception as e:
            print e
            rows = []

        products = []
        for row in rows:
            values_dict = {}
            for i in xrange(len(columns)):
                values_dict[columns[i]] = row[i]
            product = Product()
            product.set_values(values_dict)
            products.append(product)
        return products

    def get_categories(self):
        columns = Category().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Category '

        try:
            self.cursor.execute(request)
            rows = self.cursor.fetchall()

        except Exception as e:
            print e
            rows = []

        categories = []
        for row in rows:
            values_dict = {}
            for i in xrange(len(columns)):
                values_dict[columns[i]] = row[i]
            cat = Category()
            cat.set_values(values_dict)
            categories.append(cat)
        return categories

    def get_random_products(self, number_of_products):
        pass
        #try:
        #    self.cursor.execute("SELECT * from Products")
        #    count = self.cursor.rowcount
        #    rows = self.cursor.fetchall()


        #    for i in xrange(number_of_products)

        #    for n in number_of_products:
        #        random.randrange(1, count)

        #except Exception as e:
        #    print e


        #return (Product() for i in xrange(number_of_products))

    def add_ad(self, ad):
        parameters = ad.to_dict().keys():
        request = 'UPDATE Ad SET '
        for column in parameters:
            request += column + '=' + self.f + ', '
        
        request = request[0:-2]
        request += " WHERE id = " + str(ad.id)
        try:
            self.cursor.execute(request, parameters.values())
            self.db.commit()
        except Exception as e:
            print e

    def delete_ad(self, ad_id):
        try:
            self.cursor.execute("DELETE from Ad where id = %s" % ad_id)
            self.db.commit
            print("Total rows deleted: %s" % self.cursor.rowcount)
        except Exception as e:
            print e

    def get_all_ads(self):
        columns = Ad().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Ad '

        try:
            self.cursor.execute(request)
            rows = self.cursor.fetchall()

        except Exception as e:
            print e
            rows = []

        ads = []
        for row in rows:
            values_dict = {}
            for i in xrange(len(columns)):
                values_dict[columns[i]] = row[i]
            ad = Ad()
            ad.set_values(values_dict)
            ads.append(ad)
        return ads

    def save_image(self, image):

        parameters = image.to_dict().keys():
        request = 'UPDATE Image SET '
        for column in parameters:
            request += column + '=' + self.f + ', '
        
        request = request[0:-2]
        request += " WHERE id = " + str(image.id)

        try:
            self.cursor.execute(request, parameters.values())
            self.db.commit()
        except Exception as e:
            print e


        #mypic = open(image, 'rb').read()
                    
        #self.cursor.("insert into Image (Id, Bytes) values (%s, %s)",
        #                        (psycopg2.Binary(mypic),))



    def get_image(self, image_id):
        columns = Image().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Image '

        try:
            self.cursor.execute(request)
            row = self.cursor.fetchone()

        except Exception as e:
            print e
            row = None

        return row

    def delete_image(self, image_id):
        try:
            self.cursor.execute("DELETE from Image where id = %s" % image_id)
            self.db.commit
            print("Total rows deleted: %s" % self.cursor.rowcount)
        except Exception as e:
            print e
