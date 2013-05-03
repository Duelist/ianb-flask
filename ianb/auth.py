from functools import wraps

from flask import request, Response

from ianb import local_settings

def check_auth(username, password):
    return username == local_settings.username and password == local_settings.password

def authenticate():
    return Response(
    'Could not verify your access level.\n'
    'Please log in with the proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated