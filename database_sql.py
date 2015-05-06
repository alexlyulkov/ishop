sql_types = {'int':'INTEGER', 'long':'INTEGER', 'str':'TEXT', 'unicode':'TEXT', 'float':'REAL'}

from classes import Product, Ad, Category, Image
import psycopg2
import traceback
from random import randrange

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

    def add_product(self, product):
        try:
            self.cursor.execute('SELECT max(id) FROM Product')
            max_id = self.cursor.fetchone()[0]
        except Exception as e:
            print e
            print traceback.format_exc()
            max_id = None
            
        if max_id == None:
            max_id = 0
        new_id = max_id + 1
        product.id = new_id
        
        parameters = product.to_dict()
        keys = parameters.keys()
        request = 'INSERT INTO Product ('
        for key in keys:
            request += key + '=' + self.f + ', '
        request = request[0:-2]
        request += ')'
        
        try:
            self.cursor.execute(request, parameters.values())
            self.db.commit()
        except Exception as e:
            print e  
            return None
        return new_id

    def update_product(self, product):
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
            self.cursor.execute("DELETE from Product where Id = %s" % product_id)
            self.db.commit
            print("Total rows deleted: %s" % self.cursor.rowcount)
        except Exception as e:
            print e


    def add_category(self, category):
        try:
            self.cursor.execute('SELECT max(id) FROM Category')
            max_id = self.cursor.fetchone()[0]
        except Exception as e:
            print e
            print traceback.format_exc()
            max_id = None
            
        if max_id == None:
            max_id = 0
        new_id = max_id + 1
        category.id = new_id
        
        parameters = category.to_dict()
        keys = parameters.keys()
        request = 'INSERT INTO Category ('
        for key in keys:
            request += key + '=' + self.f + ', '
        request = request[0:-2]
        request += ')'
        
        try:
            self.cursor.execute(request, parameters.values())
            self.db.commit()
        except Exception as e:
            print e  
            return None
        return new_id
        
    def update_category(self, category):
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

        if (int(max_id) < int(number_of_product)):
            return None

        request = 'SELECT * from Product OFFSET RANDOM() * (SELECT COUNT(*) FROM Product) LIMIT '
        request += int(number_of_products)
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

    def add_ad(self, ad):
        try:
            self.cursor.execute('SELECT max(id) FROM Ad')
            max_id = self.cursor.fetchone()[0]
        except Exception as e:
            print e
            print traceback.format_exc()
            max_id = None
            
        if max_id == None:
            max_id = 0
        new_id = max_id + 1
        ad.id = new_id
        
        parameters = ad.to_dict()
        keys = parameters.keys()
        request = 'INSERT INTO Ad ('
        for key in keys:
            request += key + '=' + self.f + ', '
        request = request[0:-2]
        request += ')'
        
        try:
            self.cursor.execute(request, parameters.values())
            self.db.commit()
        except Exception as e:
            print e  
            return None
        return new_id

    def update_ad(self, ad):
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

    def add_image(self, image):
        try:
            self.cursor.execute('SELECT max(id) FROM Image')
            max_id = self.cursor.fetchone()[0]
        except Exception as e:
            print e
            print traceback.format_exc()
            max_id = None
            
        if max_id == None:
            max_id = 0
        new_id = max_id + 1
        image.id = new_id
        
        parameters = image.to_dict()
        keys = parameters.keys()
        request = 'INSERT INTO Image ('
        for key in keys:
            request += key + '=' + self.f + ', '
        request = request[0:-2]
        request += ')'
        
        try:
            self.cursor.execute(request, parameters.values())
            self.db.commit()
        except Exception as e:
            print e  
            return None
        return new_id

    def update_image(self, image):

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
