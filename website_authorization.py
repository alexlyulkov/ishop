from hashlib import sha256
from flask import Response, request
from functools import wraps

def requires_auth(f):
    '''Enables authorization request'''
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or \
           not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    try:
        password_file = open('key','r')
        valid_hash = password_file.read()
        password_file.close()
        h = sha256()
        h.update('pwkfwkfwpekf46436')
        h.update(password)
        user_hash = h.hexdigest()
        return (username == 'user') and (user_hash == valid_hash)
    except Exception as e:
        print e
        return False
    
def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    "You don't have access to this page.\n "
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def change_password(new_password):
    h = sha256()
    h.update('pwkfwkfwpekf46436')
    h.update(new_password)
    password_hash = h.hexdigest()

    password_file = open('key', 'w')
    password_file.write(password_hash)
    password_file.close()

