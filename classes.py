from hashlib import sha256

class Category():
    def __init__(self, init_values = None):
        self.id = 1
        self.name = 'category1'
        if init_values != None:
            for key in init_values.keys():
                setattr(self, key, init_values[key])
                
    def set_values(self, values):
        for key in values.keys():
            setattr(self, key, values[key])

    def to_dict(self):
        return self.__dict__

class Product():
    def __init__(self, init_values = None):
        self.id = -1
        self.name = ""
        self.description = ""
        self.brand = ""
        self.price = 0
        self.category = 1
        self.images_ids = []
        if init_values != None:
            for key in init_values.keys():
                setattr(self, key, init_values[key])
                
    def set_values(self, values):
        for key in values.keys():
            setattr(self, key, values[key])

    def to_dict(self):
        return self.__dict__  

class Ad():
    def __init__(self, init_values = None):
        self.id = -1
        self.image_id = 1
        self.name = ''
        if init_values != None:
            for key in init_values.keys():
                setattr(self, key, init_values[key])
                
    def set_values(self, values):
        for key in values.keys():
            setattr(self, key, values[key])

    def to_dict(self):
        return self.__dict__

class Image():
    def __init__(self):
        self.id = -1
        self.bytes = 'binary data'

    def set_values(self, values):
        for key in values.keys():
            setattr(self, key, values[key])

    def to_dict(self):
        return self.__dict__
        
class Order():
    def __init__(self, init_values = None):
        self.id = 1
        self.name = ''
        self.phone = ''
        self.address = ''
        self.products = []
        if init_values != None:
            for key in init_values.keys():
                setattr(self, key, init_values[key])

    def set_values(self, values):
        for key in values.keys():
            setattr(self, key, values[key])

    def to_dict(self):
        return self.__dict__

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
