import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///UNI_shop.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("/admin/indexAdmin.html")


@app.route("/chartjs")
def chartjs():
    return render_template("/admin/pages/charts/chartjs.html")


@app.route("/forms")
def forms():
    return render_template("/admin/pages/forms/basic_elements.html")


@app.route("/Proveedores")
def Proveedores():
    return render_template("/admin/pages/forms/CrearProv.html")

@app.route("/Datos")
def Datos():
    return render_template("/admin/pages/tables/basic-table.html")

@app.route("/LoginAdmin")
def LoginAdmin():
    return render_template("/admin/pages/samples/login.html")

# cliente page

@app.route("/About")
def About():
    return render_template("/cliente/about.html")

@app.route("/Blog_Details")
def Blog_Details():
    return render_template("/cliente/blog-details.html")

@app.route("/Blog")
def Blog():
    return render_template("/cliente/blog.html")

@app.route("/Check")
def Check():
    return render_template("/cliente/checkout.html")

@app.route("/ContactUs")
def ContactUs():
    return render_template("/cliente/contact.html")

@app.route("/Login")
def Login():
    return render_template("/cliente/login.html")

@app.route("/Register")
def Register():
    return render_template("/cliente/register.html")

@app.route("/ProductDetails")
def ProductDetails():
    return render_template("/cliente/shop-details.html")

@app.route("/Shop")
def Shop():
    return render_template("/cliente/shop.html")

@app.route("/Shopping_Cart")
def Shopping_Cart():
    return render_template("/cliente/shopping-cart.html")

