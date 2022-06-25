from logging.handlers import TimedRotatingFileHandler
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
        db.execute("INSERT INTO usuarios (correo, usuario, password) VALUES (?, ?, ?)", correo, usuario, password)
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
def graficos():

#a partir de aca se va a poblar la tabla de cuentas

    # ultimas_cuentas = db.execute("SELECT _____ FROM _____ TOP 5 ORDER BY fecha ASC")
    
    # tabla_cuentas = []

    # for i in ultimas_cuentas:
    #     tabla_cuentas.append(i[""])

#a partir de aca se va a poblar la tabla de resumen de egresos

    # ultimos_egresos = db.execute("SELECT _____ FROM _____ TOP 5 ORDER BY fecha ASC")
    
    # tabla_egreso = []

    # for i in ultimos_egresos:
    #     tabla_egreso.append(i[""])

#a partir de aca se va a poblar la tabla de resumen de ingresos

    # ultimos_ingresos = db.execute("SELECT _____ FROM _____ TOP 5 ORDER BY fecha ASC")
    
    # tabla_ingreso = []

    # for i in ultimos_ingresos:
    #     tabla_ingreso.append(i[""])

#a partir de aca se crea el grafico de resumen de egresos

    totales_egr = db.execute("SELECT sum(egresos.monto) AS monto, categoria_egresos.categoria_e FROM egresos \
                        JOIN categoria_egresos ON egresos.id_categoria_egr = categoria_egresos.id_categoria_egr \
                        GROUP BY categoria_e")

    categoria_egresos = [1,2,3]
    total_egresos = [1,2,3]

    for i in totales_egr:
        categoria_egresos.append(i["id_categoria_egr"])
        total_egresos.append(i["monto"])

#a partir de aca se crea el grafico de resumen de ingresos

    totales_ing = db.execute("SELECT sum(ingresos.monto) AS monto, categoria_ingresos.categoria_i FROM ingresos \
                        JOIN categoria_ingresos ON ingresos.id_categoria_ing = categoria_ingresos.id_categoria_ing \
                        GROUP BY categoria_i")

    categoria_ingresos = [5,6,7]
    total_ingresos = [5,6,7]

    for i in totales_ing:
        categoria_ingresos.append(i["id_categoria_ing"])
        total_ingresos.append(i["monto"])

    return render_template("resumen.html",categoria_ingresos=categoria_ingresos, total_ingresos=total_ingresos,categoria_egresos=categoria_egresos, total_egresos=total_egresos)

#Funcion para registrar datos de ingresos
@app.route("/ingreso_datos")
def registro_ingresos():
    
    if request.method == "POST":
        ingreso = request.form.get("ingreso_categoria")
        monto_i = request.form.get("ingreso_monto")
        moneda_i = request.form.get("moneda_ing")
        fecha_i = request.form.get("ingreso_fecha")

        db.execute("INSERT INTO _______ VALUES (?,?,?,?)",ingreso, monto_i, moneda_i, fecha_i)
        return render_template("ingreso_datos.html")

    else:
        return render_template("ingreso_datos.html")

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
@app.route("/ingreso_datos")
def registro_cuentas():

    if request.method == "POST":
        cuenta = request.form.get("cuenta_nombre")

        db.execute("INSERT INTO _______ VALUES (?)", cuenta)
        return render_template("ingreso_datos.html")

    else:
        return render_template("ingreso_datos.html")

if __name__== '__main__':
    app.run()