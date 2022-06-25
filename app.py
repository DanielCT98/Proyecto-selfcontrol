import os

from cs50 import SQL
from flask_session import Session
from flask import Flask, flash, redirect, render_template, request, session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

app = Flask(__name__)

#conexion a la base de datos
db = SQL("sqlite:///selfcontrol.db")

#clave secreta para que funcione
app.secret_key = 'super secret key'

#redirigir a la principal
@app.route("/")
def index():
    return render_template("principal.html")

#Funcion para el registro de una cuenta
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        
        usuario = request.form.get("username")
        password = request.form.get("password")
        correo = request.form.get("correo")
        confirmacion = request.form.get("confirmation")
        if password == "" or password != confirmacion:
            return render_template("error.html")
        session["id_usuario"] = db.execute("INSERT INTO usuarios (correo, usuario, password) VALUES (?, ?, ?)", correo, usuario, password)
    return render_template("register.html")

#Funcion para el inicio de sesion
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("error.html")
        elif not request.form.get("password"):
            return render_template("error.html")

        rows = db.execute("SELECT * FROM usuarios WHERE usuario = ?", request.form.get("username"))
        if len(rows) != 1 or not (rows[0]["password"], request.form.get("password")):
            return render_template("error.html")

        session["id_usuario"] = rows[0]["id_usuario"]
        return redirect("/resumen")

    else:
        return render_template("login.html")


#Funcion que crea los graficos
@app.route("/resumen")
def graficos_tablas():

#a partir de aca se va a poblar la tabla de cuentas

    ultimas_cuentas = db.execute("SELECT nombre_cuenta FROM cuentas WHERE id_usuario = ? ORDER BY id_cuenta DESC LIMIT 5", session["id_usuario"])
    

#a partir de aca se va a poblar la tabla de resumen de egresos

    ultimos_egresos = db.execute("SELECT monto, mes, categoria_e FROM egresos, categoria_egresos WHERE id_usuario = ? AND egresos.id_categoria_egr = categoria_egresos.id_categoria_egr ORDER BY id_egreso DESC;", session["id_usuario"])
    

#a partir de aca se va a poblar la tabla de resumen de ingresos

    ultimos_ingresos = db.execute("SELECT monto, mes, categoria_i FROM ingresos, categoria_ingresos WHERE id_usuario = ? AND ingresos.id_categoria_ing = categoria_ingresos.id_categoria_ing ORDER BY id_ingreso DESC;", session["id_usuario"])
    

#a partir de aca se crea el grafico de resumen de egresos

    totales_egr = db.execute("SELECT sum(monto), categoria_e FROM egresos, categoria_egresos WHERE id_usuario = ? AND egresos.id_categoria_egr = categoria_egresos.id_categoria_egr GROUP BY categoria_e;", session["id_usuario"])

    categoria_egresos = []
    total_egresos = []

    for i in totales_egr:
        categoria_egresos.append(i["categoria_e"])
        total_egresos.append(i["sum(monto)"])

#a partir de aca se crea el grafico de resumen de ingresos

    totales_ing = db.execute("SELECT sum(monto), categoria_i FROM ingresos, categoria_ingresos WHERE id_usuario = ? AND ingresos.id_categoria_ing = categoria_ingresos.id_categoria_ing GROUP BY categoria_i;", session["id_usuario"])

    categoria_ingresos = []
    total_ingresos = []

    for i in totales_ing:
        categoria_ingresos.append(i["categoria_i"])
        total_ingresos.append(i["sum(monto)"])

    return render_template("resumen.html",categoria_ingresos=categoria_ingresos, total_ingresos=total_ingresos,categoria_egresos=categoria_egresos, total_egresos=total_egresos, ultimas_cuentas=ultimas_cuentas, ultimos_egresos=ultimos_egresos, ultimos_ingresos=ultimos_ingresos)

#Funcion para registrar datos de ingresos
@app.route("/ingreso_datos")
def registro_ingresos():
    
    cuentas = db.execute("SELECT nombre_cuenta FROM cuentas WHERE id_usuario = ? ORDER BY id_cuenta ASC", session["id_usuario"])

    if request.method == "POST":
        ingreso = request.form.get("ingreso_categoria")
        monto_i = request.form.get("ingreso_monto")
        moneda_i = request.form.get("moneda_ing")
        fecha_i = request.form.get("ingreso_fecha")

        db.execute("INSERT INTO _______ VALUES (?,?,?,?)",ingreso, monto_i, moneda_i, fecha_i)
        return render_template("ingreso_datos.html")

    else:
        return render_template("ingreso_datos.html",cuentas=cuentas)

#Funcion para registrar datos de egresos
@app.route("/ingreso_datos")
def registro_egresos():

    if request.method == "POST":
        egreso = request.form.get("egreso_categoria")
        monto_e = request.form.get("egreso_monto")
        moneda_e = request.form.get("moneda_egr")
        fecha_e = request.form.get("egreso_fecha")

        db.execute("INSERT INTO _______ VALUES (?,?,?,?)",egreso, monto_e, moneda_e, fecha_e)
        return render_template("ingreso_datos.html")

    else:
        return render_template("ingreso_datos.html")

#Funcion para registrar cuentas
@app.route("/cuentas", methods = ["POST"])
def registro_cuentas():

    cuenta = request.form.get("cuenta_nombre")

    db.execute("INSERT INTO cuentas VALUES (?,?)", session["id_usuario"], cuenta)
    return redirect("/ingreso_datos")


if __name__== '__main__':
    app.run()