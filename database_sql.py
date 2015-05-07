sql_types = {'int':'INTEGER', 'long':'INTEGER', 'str':'TEXT', 'unicode':'TEXT', 'float':'REAL', 'list':'INTEGER[]'}

from classes import *
import psycopg2
import traceback
import base64

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
        
        columns = Category().to_dict()
        del columns['id']
        request = 'CREATE TABLE IF NOT EXISTS Category '
        request += "(id SERIAL UNIQUE"
        for column, value in columns.items():
            request += ', ' + column + ' ' + \
                        sql_types[type(value).__name__]
        request += ")"
        self.cursor.execute(request)
        self.db.commit()


        columns = Image().to_dict()
        del columns['id']
        request = 'CREATE TABLE IF NOT EXISTS Image '
        request += "(id SERIAL UNIQUE, bytes TEXT)"
        self.cursor.execute(request)
        self.db.commit()
            
            
        columns = Ad().to_dict()
        del columns['id']
        request = 'CREATE TABLE IF NOT EXISTS Ad '
        request += "(id SERIAL UNIQUE"
        for column, value in columns.items():
            request += ', ' + column + ' ' + \
                        sql_types[type(value).__name__]
        request += ")"
        self.cursor.execute(request)
        self.db.commit()
            
            
        columns = Product().to_dict()
        del columns['id']
        request = 'CREATE TABLE IF NOT EXISTS Product '
        request += "(id SERIAL UNIQUE"
        for column, value in columns.items():
            request += ', ' + column + ' ' + \
                        sql_types[type(value).__name__]
        request += ")"
        self.cursor.execute(request)
        self.db.commit()
            
            
        columns = Order().to_dict()
        del columns['id']
        request = 'CREATE TABLE IF NOT EXISTS Orders '
        request += "(id SERIAL UNIQUE"
        for column, value in columns.items():
            request += ', ' + column + ' ' + \
                        sql_types[type(value).__name__]
        request += ")"
        self.cursor.execute(request)
        self.db.commit()

    def cleanup_db(self):
        try:
            self.cursor.execute("DROP TABLE IF EXISTS Orders")
            self.cursor.execute("DROP TABLE IF EXISTS Product")
            self.cursor.execute("DROP TABLE IF EXISTS Ad")
            self.cursor.execute("DROP TABLE IF EXISTS Image")
            self.cursor.execute("DROP TABLE IF EXISTS Category")
            self.db.commit()
        finally:
            self.db.close()
            
    def add_product(self, product):
        parameters = product.to_dict()
        del parameters['id']
        keys = parameters.keys()
        request = 'INSERT INTO Product ('
        for column in parameters.keys():
            request += column + ', '
        request = request[0:-2] + ') VALUES ('
        
        for column in parameters.keys():
            request += self.f + ','
        request = request[0:-1] + ')'
        '''for key in keys:
            request += key + '=' + self.f + ', '
    
            if (type(parameters[key]).__name__=='list'):
                parameters[key] = 'ARRAY' + parameters[key]
                
        request = request[0:-2]
        request += ')'''
        val = ""

        self.cursor.execute(request, parameters.values())
        #self.cursor.execute("SELECT LASTVAL()")
        #val = self.cursor.fetchone()[1]
        self.db.commit()
        #return val

    def update_product(self, product):
        parameters = product.to_dict()
        keys = parameters.keys()
        request = 'UPDATE Product SET '
        for key in keys:
            request += key + '=' + self.f + ', '
        request = request[0:-2]
        request += " WHERE id = " + str(product.id)

        self.cursor.execute(request, parameters.values())
        self.db.commit()
        
    def load_product(self, product_id):
        columns = Product().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Product '
        request += ' WHERE id = '
        request += str(product_id)

        self.cursor.execute(request)
        row = self.cursor.fetchone()

        product = Product()
        values_dict = {}
        for i in xrange(len(columns)):
            values_dict[columns[i]] = row[i]
        product.set_values(values_dict)
        return product

    def load_products(self):
        columns = Product().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Product '
        rows = []

        self.cursor.execute(request)
        rows = self.cursor.fetchall()

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
        self.cursor.execute("DELETE from Product where id = %s" % product_id)
        self.db.commit()



    def add_category(self, category):
        parameters = category.to_dict()
        del parameters['id']
        keys = parameters.keys()
        request = 'INSERT INTO Category ('
        for column in parameters.keys():
            request += column + ', '
        request = request[0:-2] + ') VALUES ('
        
        for column in parameters.keys():
            request += self.f + ','
        request = request[0:-1] + ')'
        val = ""

        self.cursor.execute(request, parameters.values())
        #self.cursor.execute("SELECT LASTVAL()")
        #val = self.cursor.fetchone()[1]
        self.db.commit()
        #return val
        
    def update_category(self, category):
        parameters = category.to_dict()
        keys = parameters.keys()
        request = 'UPDATE Category SET '
        for key in keys:
            request += key + '=' + self.f + ', '
        
        request = request[0:-2]
        request += " WHERE id = " + str(category.id)
        self.cursor.execute(request, parameters.values())
        self.db.commit()

    def delete_category(self, category_id):
        self.cursor.execute("DELETE from Category where id = %s" % category_id)
        self.db.commit()

    def load_category_products(self, category_id, order_by = id, brands_filter = []):
        columns = Product().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Product '
        request += 'WHERE category = '
        request += str(category_id)

        if len(brands_filter)>0:
            request += ' AND ('
            for brand in brands_filter:
                request += 'brand = ' + brand + ' OR '
            request = request[0:-4] + ')'
        if order_by:
            request += ' ORDER BY ' + str(order_by) + ' ASC'
            
        rows = []
        self.cursor.execute(request)
        rows = self.cursor.fetchall()

        products = []
        for row in rows:
            values_dict = {}
            for i in xrange(len(columns)):
                values_dict[columns[i]] = row[i]
            product = Product()
            product.set_values(values_dict)
            products.append(product)
        return products
        
    def get_category_brands(self, category_id):
        request = 'SELECT DISTINCT brand FROM Product WHERE category = '
        request += str(category_id)
        self.cursor.execute(request)
        rows = self.cursor.fetchall()
        brands = [x[0] for x in rows]
        return brands

    def load_categories(self):
        columns = Category().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Category '
        rows = []

        self.cursor.execute(request)
        rows = self.cursor.fetchall()

        categories = []
        for row in rows:
            values_dict = {}
            for i in xrange(len(columns)):
                values_dict[columns[i]] = row[i]
            cat = Category()
            cat.set_values(values_dict)
            categories.append(cat)
        return categories
        
    def load_category(self, category_id):
        columns = Category().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Category '
        request += ' WHERE id = '
        request += str(category_id)
        rows = []

        self.cursor.execute(request)
        rows = self.cursor.fetchall()

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
        columns = Product().to_dict().keys()
        self.cursor.execute("SELECT COUNT(*) FROM Product")
        count = self.cursor.fetchone()[0]
        
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Product '
        rows = []
        if (int(count) > int(number_of_products)):
            request += ' OFFSET RANDOM() * '
            request += count
            request += ' LIMIT '
            request += int(number_of_products)

        self.cursor.execute(request)
        rows = self.cursor.fetchall()

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
        parameters = ad.to_dict()
        del parameters['id']
        keys = parameters.keys()
        request = 'INSERT INTO Ad ('
        for column in parameters.keys():
            request += column + ', '
        request = request[0:-2] + ') VALUES ('
        
        for column in parameters.keys():
            request += self.f + ','
        request = request[0:-1] + ')'
        val = ""

        self.cursor.execute(request, parameters.values())
        #self.cursor.execute("SELECT LASTVAL()")
        #val = self.cursor.fetchone()[1]
        self.db.commit()
        #return val

    def update_ad(self, ad):
        parameters = ad.to_dict()
        keys = parameters.keys()
        request = 'UPDATE Ad SET '
        for key in keys:
            request += key + '=' + self.f + ', '
        request = request[0:-2]
        request += " WHERE id = " + str(ad.id)

        self.cursor.execute(request, parameters.values())
        self.db.commit()

    def load_ads(self):
        columns = Ad().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Ad '
        rows = []
        
        self.cursor.execute(request)
        rows = self.cursor.fetchall()


        ads = []
        for row in rows:
            values_dict = {}
            for i in xrange(len(columns)):
                values_dict[columns[i]] = row[i]
            ad = Ad()
            ad.set_values(values_dict)
            ads.append(ad)
        return ads

    def load_ad(self, ad_id):
        columns = Ad().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Ad '
        request += ' WHERE id = '
        request += str(ad_id)
        rows = []
        
        self.cursor.execute(request)
        rows = self.cursor.fetchall()

        ads = []
        for row in rows:
            values_dict = {}
            for i in xrange(len(columns)):
                values_dict[columns[i]] = row[i]
            ad = Ad()
            ad.set_values(values_dict)
            ads.append(ad)
        return ads[0]

    def delete_ad(self, ad_id):
        self.cursor.execute("DELETE from Ad where id = %s" % ad_id)
        self.db.commit()
        

    def add_image(self, image):
        #print image.bytes
        parameters = image.to_dict()
        del parameters['id']
        #parameters['bytes'] = psycopg2.Binary(images.bytes)
        keys = parameters.keys()
        request = 'INSERT INTO Image ('
        for key in keys:
            request += key + '=' + self.f + ', '
        request = request[0:-2]
        request += ')'
        request = "INSERT INTO Image(bytes) VALUES (%s) RETURNING id"
        val = ""

        #self.cursor.execute(request, parameters.values())
        self.cursor.execute(request, (base64.b64encode(image.bytes),))
        #self.cursor.execute("SELECT LASTVAL()")
        val = self.cursor.fetchone()
        val = val[0]
        self.db.commit()
            
        return val

    def update_image(self, image):
        parameters = image.to_dict().keys()
        request = 'UPDATE Image SET '
        for column in parameters:
            request += column + '=' + self.f + ', '
        
        request = request[0:-2]
        request += " WHERE id = " + str(image.id)

        self.cursor.execute(request, parameters.values())
        self.db.commit()

    def get_image(self, image_id):
        columns = Image().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Image '
        request += ' WHERE id = '
        request += str(image_id)
        row = []

        self.cursor.execute(request)
        row = self.cursor.fetchone()
        
        values_dict = {}
        for i in xrange(len(columns)):
            values_dict[columns[i]] = row[i]
        values_dict['bytes'] = base64.b64decode(values_dict['bytes'])
        ad = Ad()
        ad.set_values(values_dict)
        return ad

    def delete_image(self, image_id):
        self.cursor.execute("DELETE from Image where id = %s" % image_id)
        self.db.commit()

    def add_order(self, order):
        parameters = order.to_dict()
        del parameters['id']
        keys = parameters.keys()
        request = 'INSERT INTO Orders ('
        for column in parameters.keys():
            request += column + ', '
        request = request[0:-2] + ') VALUES ('
        
        for column in parameters.keys():
            request += self.f + ','
        request = request[0:-1] + ') RETURNING id'
        '''for key in keys:
            request += key + '=' + self.f + ', '
            if (type(parameters[key]).__name__=='list'):
                parameters[key] = 'ARRAY' + parameters[key]
        request = request[0:-2]
        request += ') RETURNING id'''
        val = ""

        self.cursor.execute(request, parameters.values())
        #self.cursor.execute("SELECT LASTVAL()")
        val = self.cursor.fetchone()[0]
        self.db.commit()
        
        return val

    def update_order(self, order):
        parameters = order.to_dict()
        keys = parameters.keys()
        request = 'UPDATE Orders SET '
        for key in keys:
            request += key + '=' + self.f + ', '
        request = request[0:-2]
        request += " WHERE id = " + str(order.id)
    
        self.cursor.execute(request, parameters.values())
        self.db.commit()
        
    def load_order_products(self, order_id):
        columns = Product().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Product '
        request += ' WHERE '
        if len(load_order(order_id).products>0):
            for i in load_order(order_id).products:
                request += 'id = ' + i + ' OR '
            request = request[0:-4]
        
        rows = []

        self.cursor.execute(request)
        rows = self.cursor.fetchall()

        products = []
        for row in rows:
            values_dict = {}
            for i in xrange(len(columns)):
                values_dict[columns[i]] = row[i]
            product = Product()
            product.set_values(values_dict)
            products.append(product)
        return products

    def load_orders(self):
        columns = Order().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Orders '
        rows = []
        
        self.cursor.execute(request)
        rows = self.cursor.fetchall()

        orders = []
        for row in rows:
            values_dict = {}
            for i in xrange(len(columns)):
                values_dict[columns[i]] = row[i]
            order = Order()
            order.set_values(values_dict)
            orders.append(order)
        return orders

    def load_order(self, order_id):
        columns = Order().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Orders '
        request += ' WHERE id = '
        request += str(order_id)
        rows = []

        self.cursor.execute(request)
        rows = self.cursor.fetchall()

        orders = []
        for row in rows:
            values_dict = {}
            for i in xrange(len(columns)):
                values_dict[columns[i]] = row[i]
            order = Order()
            order.set_values(values_dict)
            orders.append(order)
        return orders[0]
        
    def delete_order(self, order_id):
        self.cursor.execute("DELETE from Orders where id = %s" % order_id)
        self.db.commit()
