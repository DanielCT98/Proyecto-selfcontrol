from logging.handlers import TimedRotatingFileHandler
import os

from cs50 import SQL
from flask_session import Session
from flask import Flask, flash, redirect, render_template, request, session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

app = Flask(__name__)

db = SQL("sqlite:///prueba.db")

@app.route("/")
def index():
    return render_template("principal.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        
        usuario = request.form.get("username")
        password = request.form.get("password")
        correo = "a@a.com"
        confirmacion = request.form.get("confirmation")
        if password == "" or password != confirmacion:
            return render_template("error.html")
        db.execute("INSERT INTO usuario_uat (correo, usuario, pass) VALUES (?, ?, ?)", correo, usuario, password)
    #return redirect("/")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    #session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("error.html")
        elif not request.form.get("password"):
            return render_template("error.html")

        rows = db.execute("SELECT * FROM usuario_uat WHERE usuario = ?", request.form.get("username"))
        if len(rows) != 1 or not (rows[0]["pass"], request.form.get("password")):
            return render_template("error.html")

        session["id_usuario"] = rows[0]["id"]
        return redirect("/resumen")

    else:
        return render_template("login.html")


@app.route("/resumen")
def graficos():
    totales = db.execute("SELECT sum(monto) AS monto, categoria FROM egresos GROUP BY categoria")

    categoria = []
    val_totales = []

    for i in totales:
        categoria.append(i["categoria"])
        val_totales.append(i["monto"])

    return render_template("resumen.html",categoria=categoria, val_totales=val_totales)

if __name__== '__main__':
    app.run()