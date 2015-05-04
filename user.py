from hashlib import sha256



class User():
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
        employee.password_hash = password_hash
