import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from flask import jsonify
from flask_cors import CORS, cross_origin
import cloudinary
from helpers import login_required

# Configure application
app = Flask(__name__)
CORS(app)
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


@app.route("/Proveedores", methods=["POST","GET"])
def Proveedores():
    if request.method == "POST":
        print(request.form.get("Nombre1"))
        print(request.form.get("Nombre2"))
        print(request.form.get("Apellido1"))
        print(request.form.get("Apellido2"))
        print(request.form.get("Direccion"))
        print(request.form.get("Telefono"))
        print(request.form.get("Ruc"))
        print(request.form.get("Correo"))
        if not request.form.get("Nombre1") or not request.form.get("Nombre2") or not request.form.get("Apellido1") or not request.form.get("Apellido2") or not request.form.get("Direccion") or not request.form.get("Telefono") or not request.form.get("Ruc") or not request.form.get("Correo"):
            # error = "SI"
            flash("Faltan Campos por llenar")
            return render_template("/admin/pages/forms/CrearProv.html")
        Nombre1 = request.form.get("Nombre1")
        Nombre2 = request.form.get("Nombre2")
        Apellido1 = request.form.get("Apellido1")
        Apellido2 = request.form.get("Apellido2")
        Direccion = request.form.get("Direccion")
        Telefono = request.form.get("Telefono")
        Ruc = request.form.get("Ruc")
        Correo = request.form.get("Correo")
        db.execute("INSERT INTO Proveedor (PrimerNombre, SegundoNombre, PrimerApellido, SegundoApellido, Direccion, Telefono, RUC, Correo) VALUES (?,?,?,?,?,?,?,?)", Nombre1, Nombre2, Apellido1, Apellido2, Direccion, Telefono, Ruc, Correo)
        return redirect("/Proveedores")
    else:
        return render_template("/admin/pages/forms/CrearProv.html")

@app.route("/DatosProveedor")
def DatosProveedor():
    Proveedor = db.execute("SELECT * FROM Proveedor")
    print(Proveedor)
    return render_template("/admin/pages/tables/basic-table.html",Proveedor=Proveedor)

@app.route("/DatosMarca")
def DatosMarca():
    Marca = db.execute("SELECT * FROM Marca")
    return render_template("/admin/pages/tables/Marca.html",Marca=Marca)

@app.route("/Marcas")
def Marcas():
    return render_template("/admin/pages/forms/CrearMarca.html")

@app.route("/DatosCategoria")
def DatosCategoria():
    Categoria = db.execute("SELECT * FROM Categoria")
    return render_template("/admin/pages/tables/Categoria.html",Categoria=Categoria)

@app.route("/Compra")
def Compra():
    return render_template("/admin/pages/forms/Compra.html")

@app.route("/DetalleCompra")
def DetalleCompra():
    return render_template("/admin/pages/forms/Detalle_Compra.html")

@app.route("/DatosCompra")
def DatosCompra():
    return render_template("/admin/pages/tables/Compra.html")

@app.route("/Productos", methods=["POST","GET"])
def Productos():
    if request.method == "POST":
        print("url ", request.form.get("url"))
        print("prdocuto: ", request.form.get("producto"))
        print("precio ", request.form.get("precio"))
        print("cantidad ", request.form.get("cantidad"))

        #return render_template("/admin/pages/forms/CrearProd.html",CargarMarca=CargarMarca,CargarCategoria=CargarCategoria, aviso=error)
        Producto = request.form.get("producto")
        Precio = request.form.get("precio")
        Cantidad = request.form.get("cantidad")
        Url = request.form.get("url")
        Marca = request.form.get("idMarca")
        Categoria = request.form.get("idCategoria")

        if not Producto or not Precio or not Cantidad or not Url or not Marca or not Categoria:
            flash("Faltan Campos por llenar")
            return redirect("/Productos")

        db.execute("INSERT INTO Producto (idMarca, idCategoria, NombreProducto, Precio, Cantidad, urlImg) VALUES (?,?,?,?,?,?)", Marca, Categoria, Producto, Precio, Cantidad, Url)
        return redirect("/Productos")
    else:
        CargarMarca = db.execute("SELECT * FROM Marca")
        CargarCategoria = db.execute("SELECT * FROM Categoria")
        return render_template("/admin/pages/forms/CrearProd.html",CargarMarca=CargarMarca,CargarCategoria=CargarCategoria)

@app.route("/DatosProductos")
def DatosProductos():
    Productos = db.execute("SELECT * FROM Producto")
    return render_template("/admin/pages/tables/Productos.html",Productos=Productos)

@app.route("/Categorias")
def Categorias():
     if request.method == "POST":
        print(request.form.get("Catego"))
        if not request.form.get("Catego"):
            # error = "SI"
            flash("Faltan Campos por llenar")
            return render_template("/admin/pages/forms/CrearCategoria.html")
        Catego = request.form.get("Catego")
        db.execute("INSERT INTO Categoria (Categoria) VALUES (?)", Catego)
        return redirect("/Categorias")
     else:
        return render_template("/admin/pages/forms/CrearCategoria.html")

@app.route("/LoginAdmin")
def LoginAdmin():
    return render_template("/admin/pages/samples/login.html")

@app.route("/Contact")
def Contact():
    return render_template("/admin/pages/Contact/Contact.html")

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

@app.route("/img")
def img():
    return render_template("/admin/pages/upload/img.html")

@app.route("/upload", methods=["POST"])
def upload():
    url = request.form.get("url")
    return url
