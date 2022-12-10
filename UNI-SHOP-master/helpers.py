import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if session.get("user_id") is None:
            return redirect("/Login")

        if session.get("Rol") == 1:
            print("entro2")
            return "No es admin"
        return f(*args, **kwargs)
    return decorated_function

def login_rol(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("entro1")
        if session.get("Rol") is None:
            return redirect("/login")

        if session.get("Rol") == 1:
            print("entro2")
            return "No es admin"
        print("entro3")
        return f(*args, **kwargs)
    return decorated_function

