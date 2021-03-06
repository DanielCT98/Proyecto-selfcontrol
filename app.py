import os
from xml.etree.ElementTree import TreeBuilder

from cs50 import SQL
from flask_session import Session
from flask import Flask, flash, redirect, render_template, request, session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

app = Flask(__name__)

app.jinja_env.filters['zip'] = zip

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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
        session["id_usuario"] = db.execute("INSERT INTO usuarios (correo, usuario, password) VALUES (?, ?, ?)", correo, usuario, generate_password_hash(password))
        session["usuario_dato"]=usuario
    return render_template("register.html")

#Funcion para el inicio de sesion
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("error.html")
        elif not request.form.get("password"):
            return redirect("/error")

        rows = db.execute("SELECT * FROM usuarios WHERE usuario = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return redirect("/error")

        session["id_usuario"] = rows[0]["id_usuario"]
        session["usuario_dato"]= request.form.get("username")
        return redirect("/resumen")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

#Funcion que crea los graficos
@app.route("/resumen")
def graficos_tablas():

    resumen_ingresos = db.execute("SELECT nombre_cuenta, sum(monto) as 'Ingresos' FROM cuentas, ingresos WHERE ingresos.id_usuario = ? AND cuentas.id_cuenta = ingresos.id_cuenta GROUP BY nombre_cuenta;", session["id_usuario"])

    resumen_egresos = db.execute("SELECT nombre_cuenta, sum(monto) as 'Egresos' FROM cuentas, egresos WHERE egresos.id_usuario = ? AND cuentas.id_cuenta = egresos.id_cuenta GROUP BY nombre_cuenta;", session["id_usuario"])

    resumen_cuentas = []

    """ for i,j in zip(resumen_ingresos, resumen_egresos):
        
        if i["nombre_cuenta"] == j["nombre_cuenta"]:
            resumen_cuentas.append(i["nombre_cuenta"])
            resumen_cuentas.append(i["Ingresos"] - j["Egresos"]) """

    #Cordobas

    consolidado_ingresos_nio = db.execute("SELECT sum(monto) AS 'Total de ingresos NIO' FROM ingresos WHERE id_usuario = ? AND moneda = 'NIO';", session["id_usuario"])
    consolidado_egresos_nio = db.execute("SELECT sum(monto) AS 'Total de egresos NIO' FROM egresos WHERE id_usuario = ? AND moneda = 'NIO' ;", session["id_usuario"])


    saldo_nio= []
    if consolidado_ingresos_nio[0]["Total de ingresos NIO"] != None and consolidado_egresos_nio[0]["Total de egresos NIO"] != None:
        for k,l in zip(consolidado_ingresos_nio, consolidado_egresos_nio):
            saldo_nio.append(k["Total de ingresos NIO"] - l["Total de egresos NIO"])

    print(saldo_nio)

        #Dolares

    consolidado_ingresos_usd = db.execute("SELECT sum(monto) AS 'Total de ingresos USD' FROM ingresos WHERE id_usuario = ? AND moneda = 'USD';", session["id_usuario"])
    consolidado_egresos_usd = db.execute("SELECT sum(monto) AS 'Total de egresos USD' FROM egresos WHERE id_usuario = ? AND moneda = 'USD' ;", session["id_usuario"])


    saldo_usd= []
    if consolidado_ingresos_usd[0]["Total de ingresos USD"] != None and consolidado_egresos_usd[0]["Total de egresos USD"] != None:
        for k,l in zip(consolidado_ingresos_usd, consolidado_egresos_usd):
            saldo_usd.append(k["Total de ingresos USD"] - l["Total de egresos USD"])

    print(saldo_usd)


#a partir de aca se va a poblar la tabla de cuentas

    ultimas_cuentas = db.execute("SELECT nombre_cuenta FROM cuentas WHERE id_usuario = ? ORDER BY id_cuenta DESC LIMIT 5", session["id_usuario"])   

#a partir de aca se va a poblar la tabla de resumen de egresos

    ultimos_egresos = db.execute("SELECT monto, mes, categoria_e, moneda FROM egresos, categoria_egresos WHERE id_usuario = ? AND egresos.id_categoria_egr = categoria_egresos.id_categoria_egr ORDER BY id_egreso DESC  LIMIT 5;", session["id_usuario"])   

#a partir de aca se va a poblar la tabla de resumen de ingresos

    ultimos_ingresos = db.execute("SELECT monto, mes, categoria_i, moneda FROM ingresos, categoria_ingresos WHERE id_usuario = ? AND ingresos.id_categoria_ing = categoria_ingresos.id_categoria_ing ORDER BY id_ingreso DESC LIMIT 5;", session["id_usuario"])   

#a partir de aca se crea el grafico de resumen de egresos NIO

    totales_egr = db.execute("SELECT sum(monto), categoria_e FROM egresos, categoria_egresos WHERE id_usuario = ? AND egresos.id_categoria_egr = categoria_egresos.id_categoria_egr AND moneda = 'NIO' GROUP BY categoria_e;", session["id_usuario"])

    categoria_egresos = []
    total_egresos = []

    for i in totales_egr:
        categoria_egresos.append(i["categoria_e"])
        total_egresos.append(i["sum(monto)"])

#a partir de aca se crea el grafico de resumen de ingresos NIO

    totales_ing = db.execute("SELECT sum(monto), categoria_i FROM ingresos, categoria_ingresos WHERE id_usuario = ? AND ingresos.id_categoria_ing = categoria_ingresos.id_categoria_ing AND moneda = 'NIO' GROUP BY categoria_i;", session["id_usuario"])

    categoria_ingresos = []
    total_ingresos = []

    for i in totales_ing:
        categoria_ingresos.append(i["categoria_i"])
        total_ingresos.append(i["sum(monto)"])

#a partir de aca se crea el grafico de resumen de egresos USD

    totales_egr_usd = db.execute("SELECT sum(monto), categoria_e FROM egresos, categoria_egresos WHERE id_usuario = ? AND egresos.id_categoria_egr = categoria_egresos.id_categoria_egr AND moneda = 'USD' GROUP BY categoria_e;", session["id_usuario"])

    categoria_egresos_usd = []
    total_egresos_usd = []

    for i in totales_egr_usd:
        categoria_egresos_usd.append(i["categoria_e"])
        total_egresos_usd.append(i["sum(monto)"])

#a partir de aca se crea el grafico de resumen de ingresos USD

    totales_ing_usd = db.execute("SELECT sum(monto), categoria_i FROM ingresos, categoria_ingresos WHERE id_usuario = ? AND ingresos.id_categoria_ing = categoria_ingresos.id_categoria_ing AND moneda = 'USD' GROUP BY categoria_i;", session["id_usuario"])

    categoria_ingresos_usd = []
    total_ingresos_usd = []

    for i in totales_ing_usd:
        categoria_ingresos_usd.append(i["categoria_i"])
        total_ingresos_usd.append(i["sum(monto)"])

#a partir de aca se crea el grafico de resumen mensual promedio de ingresos en cordobas

    mensuales_ing = db.execute("SELECT mes, avg(monto) FROM ingresos WHERE id_usuario = ? AND moneda = 'NIO' GROUP BY mes;", session["id_usuario"])

    meses = []
    ingresos_mes = []

    for i in mensuales_ing:
        meses.append(i["mes"])
        ingresos_mes.append(i["avg(monto)"])

#a partir de aca se crea el grafico de resumen mensual promedio de ingresos en dolares

    mensuales_ing_usd = db.execute("SELECT mes, avg(monto) FROM ingresos WHERE id_usuario = ? AND moneda = 'USD' GROUP BY mes;", session["id_usuario"])

    meses_usd = []
    ingresos_mes_usd = []

    for i in mensuales_ing_usd:
        meses_usd.append(i["mes"])
        ingresos_mes_usd.append(i["avg(monto)"])

    return render_template("resumen.html", meses_usd=meses_usd ,ingresos_mes_usd=ingresos_mes_usd ,total_egresos_usd=total_egresos_usd, total_ingresos_usd=total_ingresos_usd, categoria_egresos_usd=categoria_egresos_usd, categoria_ingresos_usd=categoria_ingresos_usd, consolidado_ingresos_usd = consolidado_ingresos_usd , consolidado_egresos_usd = consolidado_egresos_usd ,saldo_usd = saldo_usd,tam = range(1 ,len(ultimos_ingresos)+1), usuario=session["usuario_dato"], saldo_nio=saldo_nio ,consolidado_ingresos_nio = consolidado_ingresos_nio ,consolidado_egresos_nio = consolidado_egresos_nio ,resumen_cuentas = resumen_cuentas, meses=meses, ingresos_mes=ingresos_mes,categoria_ingresos=categoria_ingresos, total_ingresos=total_ingresos,categoria_egresos=categoria_egresos, total_egresos=total_egresos, ultimas_cuentas=ultimas_cuentas, ultimos_egresos=ultimos_egresos, ultimos_ingresos=ultimos_ingresos)

#funcion para redirigir al ingreso de datos
@app.route("/ingreso_datos")
def registros():
    cuentas = db.execute("SELECT nombre_cuenta FROM cuentas WHERE id_usuario = ? ORDER BY id_cuenta ASC;", session["id_usuario"])
    
    return render_template("ingreso_datos.html", cuentas=cuentas)

@app.route("/error")
def error():
    return render_template("error.html")

#Funcion para registrar datos de ingresos
@app.route("/ingresos", methods = ["POST"])
def registro_ingresos():    

        ingreso = request.form.get("ingreso_categoria")
        monto_i = request.form.get("ingreso_monto")
        moneda_i = request.form.get("moneda_ing")
        fecha_i = request.form.get("ingreso_fecha")
        cuenta_i = db.execute("SELECT id_cuenta FROM cuentas WHERE id_usuario = ? AND nombre_cuenta = ?;", session["id_usuario"], request.form.get("ingreso_cuenta"))
        cuenta_ing = cuenta_i[0]["id_cuenta"]

        db.execute("INSERT INTO ingresos (id_usuario, id_cuenta, id_categoria_ing, monto, moneda, mes) VALUES (?,?,?,?,?,?);",session["id_usuario"],cuenta_ing,ingreso, monto_i, moneda_i, fecha_i)
        return redirect("/ingreso_datos")

#Funcion para registrar datos de egresos
@app.route("/egresos", methods = ["POST"])
def registro_egresos():

        egreso = request.form.get("egreso_categoria")
        monto_e = request.form.get("egreso_monto")
        moneda_e = request.form.get("moneda_egr")
        fecha_e = request.form.get("egreso_fecha")
        cuenta_e = db.execute("SELECT id_cuenta FROM cuentas WHERE id_usuario = ? AND nombre_cuenta = ?;", session["id_usuario"], request.form.get("egreso_cuenta"))
        cuenta_egr = cuenta_e[0]["id_cuenta"]

        db.execute("INSERT INTO egresos (id_usuario, id_cuenta, id_categoria_egr, monto, moneda, mes) VALUES (?,?,?,?,?,?);",session["id_usuario"],int(cuenta_egr),egreso, monto_e, moneda_e, fecha_e)
        return redirect("/ingreso_datos")

#Funcion para registrar cuentas
@app.route("/cuentas", methods = ["POST"])
def registro_cuentas():

    cuenta = request.form.get("cuenta_nombre")
    db.execute("INSERT INTO cuentas (id_usuario, nombre_cuenta) VALUES (?,?)", session["id_usuario"], cuenta)
    return redirect("/ingreso_datos")


if __name__== '__main__':
    app.run()