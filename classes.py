from hashlib import sha256

class Category():
    def __init__(self, init_values = None):
        self.id = 1
        self.name = 'category1'
        if init_values != None:
            for key in init_values.keys():
                setattr(self, key, init_values[key])


class Product():
    def __init__(self, init_values = None):
        self.id = 1
        self.name = "product1"
        self.description = "good product"
        self.brand = "nike"
        self.price = 123
        self.category = 1
        self.images_ids = [1]
        if init_values != None:
            for key in init_values.keys():
                setattr(self, key, init_values[key])

class Ad():
    def __init__(self, init_values = None):
        self.id = 1
        self.image_id = 2
        self.name = 'some ad name'
        if init_values != None:
            for key in init_values.keys():
                setattr(self, key, init_values[key])

class Image():
    def __init__(self):
        self.id = 1
        self.bytes = 'binary data'

class Order():
    def __init__(self, init_values = None):
        self.id = 1
        self.name = 'some client name'
        self.phone = '+7 123'
        self.address = 'abc'
        self.products = [1,5,7]
        if init_values != None:
            for key in init_values.keys():
                setattr(self, key, init_values[key])



'''class User():
    def __init__(self):
        self.name = "user1"
        self.email = "user1@abc.com"
        self.password_hash = 'qwer_fake_initial_password'

    def check_password(self, employee, password):
        valid_hash = self.password_hash
        h = sha256()
        h.update('eoijfo3ir09jdf')
        h.update(password)
        new_hash = h.hexdigest()
        return valid_hash == new_hash


    def set_password(self, employee, new_password):
        h = sha256()
        h.update('eoijfo3ir09jdf')
        h.update(new_password)
        password_hash = h.hexdigest()
        employee.password_hash = password_hash'''
