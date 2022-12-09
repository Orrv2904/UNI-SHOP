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
    rows = db.execute("SELECT Productos.*, Categorias.Categoria  FROM Productos INNER JOIN Categorias ON Productos.idCategoria = Categorias.idCategoria")
    #print(rows)
    return render_template("index.html", rows=rows)

@app.route("/ListoComprar/<string:id>")
def ListoComprar(id):
    return id



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
        print(request.form.get("Nombre"))
        print(request.form.get("Direccion"))
        print(request.form.get("Telefono"))
        print(request.form.get("Ruc"))
        print(request.form.get("Correo"))
        print(request.form.get("RazonSocial"))
        if not request.form.get("Nombre") or not request.form.get("Direccion") or not request.form.get("Telefono") or not request.form.get("Ruc") or not request.form.get("Correo") or not request.form.get("RazonSocial"):
            # error = "SI"
            flash("Faltan Campos por llenar")
            return render_template("/admin/pages/forms/CrearProv.html")
        Nombre = request.form.get("Nombre")
        Direccion = request.form.get("Direccion")
        Telefono = request.form.get("Telefono")
        Ruc = request.form.get("Ruc")
        Correo = request.form.get("Correo")
        RazonSocial = request.form.get("RazonSocial")
        db.execute("INSERT INTO Proveedores (Nombre, Direccion, Telefono, RUC, Correo, RazonSocial) VALUES (?,?,?,?,?,?)", Nombre, Direccion, Telefono, Ruc, Correo, RazonSocial)
        return redirect("/Proveedores")
    else:
        return render_template("/admin/pages/forms/CrearProv.html")

@app.route("/DatosProveedor")
def DatosProveedor():
    Proveedor = db.execute("SELECT * FROM Proveedores")
    print(Proveedor)
    return render_template("/admin/pages/tables/basic-table.html",Proveedor=Proveedor)

@app.route("/DatosMarca")
def DatosMarca():
    Marca = db.execute("SELECT * FROM Marcas")
    return render_template("/admin/pages/tables/Marca.html",Marca=Marca)

@app.route("/Marcas", methods=["POST","GET"])
def Marcas():
    if request.method == "POST":
        print(request.form.get("marca"))
        if not request.form.get("marca"):
            flash("Faltan Campos por llenar")
            return render_template("/admin/pages/forms/CrearMarca.html")
        marca = request.form.get("marca")
        db.execute("INSERT INTO Marcas (Marca) VALUES (?)", marca)
        return redirect("/Marcas")
    else:
        return render_template("/admin/pages/forms/CrearMarca.html")

@app.route("/DatosCategoria")
def DatosCategoria():
    Categoria = db.execute("SELECT * FROM Categorias")
    return render_template("/admin/pages/tables/Categoria.html",Categoria=Categoria)

@app.route("/Compra", methods=["POST","GET"])
def Compra():
    if request.method == "POST":
        print("fecha", request.form.get("fecha"))
        print("proveedores", request.form.get("idProveedor"))
        print("estado", request.form.get("idEstado"))

        Proveedores = request.form.get("idProveedor")
        Fecha = request.form.get("fecha")
        Estado = request.form.get("idEstado")

        if not Fecha or not Proveedores or not Estado:
            flash("Faltan Campos por llenar")
            return redirect("/Compra")
        db.execute("INSERT INTO Compras (idProveedor, Fecha, idEstado) VALUES (?,?,?)", Proveedores, Fecha, Estado)
        return redirect("/Compra")
    else:
        CargarProveedor = db.execute("SELECT * FROM Proveedores")
        CargarEstado = db.execute("SELECT * FROM Estados")
        return render_template("/admin/pages/forms/Compra.html",CargarProveedor=CargarProveedor,CargarEstado=CargarEstado)

    #return render_template("/admin/pages/forms/Compra.html")

@app.route("/DetalleCompra", methods=["POST","GET"])
def DetalleCompra():
    if request.method == "POST":
        print("precio ", request.form.get("Precio"))
        print("cantidad: ", request.form.get("Cantidad"))
        print("descuento: ", request.form.get("Descuento"))
        print("iva: ", request.form.get("IVA"))
        print("subtotal: ", request.form.get("SubTotal"))
        print("total: ", request.form.get("Total"))
        print("producto: ", request.form.get("idProducto"))
        print("compra: ", request.form.get("idCompra"))

        Compra = int(request.form.get("idCompra"))
        Producto = int(request.form.get("idProducto"))
        Precio = float(request.form.get("Precio"))
        Cantidad = int(request.form.get("Cantidad"))
        Descuento = float(request.form.get("Descuento"))
        IVA = float(request.form.get("IVA"))
        SubTotal = float(request.form.get("SubTotal"))
        Total = float(request.form.get("Total"))

        if not Compra or not Producto or not Precio or not Cantidad or not Descuento or not IVA or not SubTotal or not Total:
            # flash("Faltan Campos por llenar")
            print("hola mundo")
            return redirect("/DetalleCompra")
        db.execute("INSERT INTO detCompra (idCompra, idProducto, Precio, Cantidad, Descuento, IVA, Subtotal, Total) VALUES (:Compra,:Producto,:Precio,:Cantidad,:Descuento,:IVA,:SubTotal,:Total)",
        Compra=Compra, Producto=Producto, Precio=Precio, Cantidad=Cantidad, Descuento=Descuento, IVA=IVA, SubTotal=SubTotal, Total=Total)
        return redirect("/DetalleCompra")
    else:
        CargarCompra = db.execute("SELECT * FROM Compras")
        CargarProducto = db.execute("SELECT * FROM Productos")
        return render_template("/admin/pages/forms/Detalle_Compra.html",CargarCompra=CargarCompra,CargarProducto=CargarProducto)

@app.route("/DatosCompra")
def DatosCompra():
    Compra = db.execute("SELECT * FROM Compras")
    return render_template("/admin/pages/tables/Compra.html",Compra=Compra)

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

        db.execute("INSERT INTO Productos (idMarca, idCategoria, NombreProducto, Precio, Cantidad, Imagen) VALUES (?,?,?,?,?,?)", Marca, Categoria, Producto, Precio, Cantidad, Url)
        return redirect("/Productos")
    else:
        CargarMarca = db.execute("SELECT * FROM Marcas")
        CargarCategoria = db.execute("SELECT * FROM Categorias")
        return render_template("/admin/pages/forms/CrearProd.html",CargarMarca=CargarMarca,CargarCategoria=CargarCategoria)

@app.route("/DatosProductos")
def DatosProductos():
    Productos = db.execute("SELECT * FROM Productos")
    return render_template("/admin/pages/tables/Productos.html",Productos=Productos)

@app.route("/Categorias",  methods=["POST","GET"])
def Categorias():
     if request.method == "POST":
        print(request.form.get("Catego"))
        print(request.form.get("Descr"))
        if not request.form.get("Catego") or not request.form.get("Descr"):
            # error = "SI"
            flash("Faltan Campos por llenar")
            return render_template("/admin/pages/forms/CrearCategoria.html")
        Abrev = request.form.get("Abrev")
        Catego = request.form.get("Catego")
        Descr = request.form.get("Descr")
        db.execute("INSERT INTO Categorias (idCategoria, Categoria, Descipcion) VALUES (?, ?, ?)", Abrev, Catego, Descr)
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
