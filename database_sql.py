sql_types = {'int':'INTEGER', 'long':'INTEGER', 'str':'TEXT', 'unicode':'TEXT', 'float':'REAL', 'list':'INTEGER[]'}

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
        try:
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

            columns = Image().to_dict()
            del columns['id']
            
            request = 'CREATE TABLE IF NOT EXISTS Image '
            request += "(id SERIAL UNIQUE, bytes bytea)"
            self.cursor.execute(request)
            self.db.commit()
            
            columns = Order().to_dict()
            del columns['id']
            request = 'CREATE TABLE IF NOT EXISTS Order '
            request += "(id SERIAL UNIQUE"
            for column, value in columns.items():
                request += ', ' + column + ' ' + \
                           sql_types[type(value).__name__]
            request += ")"
            self.cursor.execute(request)
            self.db.commit()
            
        except Exception as e:
            print e


    def add_product(self, product):
        parameters = product.to_dict()
        del parameters['id']
        keys = parameters.keys()
        request = 'INSERT INTO Product ('
        for key in keys:
            request += key + '=' + self.f + ', '
    
            if (type(parameters[key]).__name__=='list'):
                parameters[key] = 'ARRAY' + parameters[key]
                
        request = request[0:-2]
        request += ')'
        val = ""
        try:
            self.cursor.execute(request, parameters.values())
            self.cursor.execute("SELECT LASTVAL()")
            val = self.cursor.fetchone()[1]
            self.db.commit()
        except Exception as e:
            print e  
            return None
        return val

    def update_product(self, product):
        parameters = product.to_dict()
        keys = parameters.keys()
        request = 'UPDATE Product SET '
        for key in keys:
            request += key + '=' + self.f + ', '
            if (type(parameters[key]).__name__=='list'):
                parameters[key] = 'ARRAY' + parameters[key]
        request = request[0:-2]
        request += " WHERE id = " + str(product.id)
        try:
            self.cursor.execute(request, parameters.values())
            self.db.commit()
        except Exception as e:
            print e
        
    def load_product(self, product_id):
        columns = Product().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Product '
        request += ' WHERE id = '
        request += product_id
        rows = []
        try:
            self.cursor.execute(request)
            rows = self.cursor.fetchall()
        except Exception as e:
            print e

        products = []
        for row in rows:
            values_dict = {}
            for i in xrange(len(columns)):
                values_dict[columns[i]] = row[i]
            product = Product()
            product.set_values(values_dict)
            products.append(product)
        return products

    def load_products(self):
        columns = Employee().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Product '
        rows = []
        try:
            self.cursor.execute(request)
            rows = self.cursor.fetchall()
        except Exception as e:
            print e

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
            self.db.commit()
            print("Total rows deleted: %s" % self.cursor.rowcount)
        except Exception as e:
            print e



    def add_category(self, category):
        parameters = category.to_dict()
        del parameters['id']
        keys = parameters.keys()
        request = 'INSERT INTO Category ('
        for key in keys:
            request += key + '=' + self.f + ', '
        request = request[0:-2]
        request += ')'
        val = ""
        try:
            self.cursor.execute(request, parameters.values())
            self.cursor.execute("SELECT LASTVAL()")
            val = self.cursor.fetchone()[1]
            self.db.commit()
        except Exception as e:
            print e  
            return None
        return val
        
    def update_category(self, category):
        parameters = category.to_dict()
        keys = parameters.keys()
        request = 'UPDATE Category SET '
        for key in keys:
            request += key + '=' + self.f + ', '
        
        request = request[0:-2]
        request += " WHERE id = " + str(category.id)
        try:
            self.cursor.execute(request, parameters.values())
            self.db.commit()
        except Exception as e:
            print e

    def load_category_products(self, category_id):
        columns = Employee().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Product '
        request += ' WHERE category = '
        request += category_id
        rows = []
        try:
            self.cursor.execute(request)
            rows = self.cursor.fetchall()

        except Exception as e:
            print e

        products = []
        for row in rows:
            values_dict = {}
            for i in xrange(len(columns)):
                values_dict[columns[i]] = row[i]
            product = Product()
            product.set_values(values_dict)
            products.append(product)
        return products

    def load_categories(self):
        columns = Category().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Category '
        rows = []
        try:
            self.cursor.execute(request)
            rows = self.cursor.fetchall()

        except Exception as e:
            print e

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
        request += category_id
        rows = []
        try:
            self.cursor.execute(request)
            rows = self.cursor.fetchall()

        except Exception as e:
            print e

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
        count = self.cursor.fetchone()[1]
        
        request = 'SELECT * from Product'
        rows = []
        if (int(count) > int(number_of_product)):
            request += ' OFFSET RANDOM() * '
            request += count
            request += ' LIMIT '
            request += int(number_of_products)
        try:
            self.cursor.execute(request)
            rows = self.cursor.fetchall()
        except Exception as e:
            print e

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
        for key in keys:
            request += key + '=' + self.f + ', '
        request = request[0:-2]
        request += ')'
        val = ""
        try:
            self.cursor.execute(request, parameters.values())
            self.cursor.execute("SELECT LASTVAL()")
            val = self.cursor.fetchone()[1]
            self.db.commit()
        except Exception as e:
            print e  
            return None
        return val

    def update_ad(self, ad):
        parameters = ad.to_dict()
        keys = parameters.keys()
        request = 'UPDATE Ad SET '
        for key in keys:
            request += key + '=' + self.f + ', '
        request = request[0:-2]
        request += " WHERE id = " + str(ad.id)
        try:
            self.cursor.execute(request, parameters.values())
            self.db.commit()
        except Exception as e:
            print e

    def load_ad_products(self, ad_id):
        columns = Employee().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Product '
        request += ' WHERE ad = '
        request += ad_id
        rows = []
        try:
            self.cursor.execute(request)
            rows = self.cursor.fetchall()

        except Exception as e:
            print e

        products = []
        for row in rows:
            values_dict = {}
            for i in xrange(len(columns)):
                values_dict[columns[i]] = row[i]
            product = Product()
            product.set_values(values_dict)
            products.append(product)
        return products

    def load_ads(self):
        columns = Ad().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Ad '
        rows = []
        try:
            self.cursor.execute(request)
            rows = self.cursor.fetchall()

        except Exception as e:
            print e

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
        request += ad_id
        rows = []
        try:
            self.cursor.execute(request)
            rows = self.cursor.fetchall()

        except Exception as e:
            print e

        ads = []
        for row in rows:
            values_dict = {}
            for i in xrange(len(columns)):
                values_dict[columns[i]] = row[i]
            ad = Ad()
            ad.set_values(values_dict)
            ads.append(ad)
        return ads

    def delete_ad(self, ad_id):
        try:
            self.cursor.execute("DELETE from Ad where id = %s" % ad_id)
            self.db.commit()
            print("Total rows deleted: %s" % self.cursor.rowcount)
        except Exception as e:
            print e



    def add_image(self, image):
        parameters = image.to_dict()
        del parameters['id']
        keys = parameters.keys()
        request = 'INSERT INTO Image ('
        for key in keys:
            request += key + '=' + self.f + ', '
        request = request[0:-2]
        request += ')'
        val = ""
        try:
            self.cursor.execute(request, parameters.values())
            self.cursor.execute("SELECT LASTVAL()")
            val = self.cursor.fetchone()[1]
            self.db.commit()
        except Exception as e:
            print e  
            return None
        return val

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

    def get_image(self, image_id):
        columns = Image().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Image '
        row = []
        try:
            self.cursor.execute(request)
            row = self.cursor.fetchone()
        except Exception as e:
            print e
            row = None

        values_dict = {}
        for i in xrange(len(columns)):
            values_dict[columns[i]] = row[i]
        ad = Ad()
        ad.set_values(values_dict)
        return ad

    def delete_image(self, image_id):
        try:
            self.cursor.execute("DELETE from Image where id = %s" % image_id)
            self.db.commit()
            print("Total rows deleted: %s" % self.cursor.rowcount)
        except Exception as e:
            print e



    def add_order(self, order):
        parameters = order.to_dict()
        del parameters['id']
        keys = parameters.keys()
        request = 'INSERT INTO Order ('
        for key in keys:
            request += key + '=' + self.f + ', '
            if (type(parameters[key]).__name__=='list'):
                parameters[key] = 'ARRAY' + parameters[key]
        request = request[0:-2]
        request += ')'
        val = ""
        try:
            self.cursor.execute(request, parameters.values())
            self.cursor.execute("SELECT LASTVAL()")
            val = self.cursor.fetchone()[1]
            self.db.commit()
        except Exception as e:
            print e  
            return None
        return val

    def update_order(self, order):
        parameters = order.to_dict()
        keys = parameters.keys()
        request = 'UPDATE Order SET '
        for key in keys:
            request += key + '=' + self.f + ', '
            if (type(parameters[key]).__name__=='list'):
                parameters[key] = 'ARRAY' + parameters[key]
        request = request[0:-2]
        request += " WHERE id = " + str(order.id)
        try:
            self.cursor.execute(request, parameters.values())
            self.db.commit()
        except Exception as e:
            print e
        
    def load_order_products(self, order_id):
        columns = Product().to_dict().keys()
        request = 'SELECT '
        for column in columns:
            request += column + ', '
        request = request[0:-2] + ' FROM Product '
        request += ' WHERE order = '
        request += order_id
        rows = []
        try:
            self.cursor.execute(request)
            rows = self.cursor.fetchall()
        except Exception as e:
            print e

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
        request = request[0:-2] + ' FROM Order '
        rows = []
        try:
            self.cursor.execute(request)
            rows = self.cursor.fetchall()
        except Exception as e:
            print e

        order = []
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
        request = request[0:-2] + ' FROM Order '
        request += ' WHERE id = '
        request += order_id
        rows = []
        try:
            self.cursor.execute(request)
            rows = self.cursor.fetchall()

        except Exception as e:
            print e

        orders = []
        for row in rows:
            values_dict = {}
            for i in xrange(len(columns)):
                values_dict[columns[i]] = row[i]
            order = Order()
            order.set_values(values_dict)
            orders.append(order)
        return orders
        
