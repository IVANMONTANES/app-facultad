from flask import Flask, render_template, request, flash, redirect, session
import os
from funciones import db



app = Flask(__name__)
app.secret_key = "clave_super_secreta"

@app.route("/login")
def get_login():
    if "logueado" in session:
        flash("ya esta logueado")
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/panel")
def get_panel():
    if "logueado" in session:
        return render_template("panel.html")
    else:
        flash("debe loguearse primero")
        return redirect("/")
    
@app.route("/cargar-materia")
def get_cargar_materia():
    if "logueado" in session:
        return render_template("cargar_materia.html")
    else:
        flash("no esta logueado")
        return redirect("/")
    
@app.route("/")
def get_index():

    if "logueado" in session:
        return redirect("/panel")
    else:
        return redirect("/login")
    
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
    





# atrapar rutas indeseadas #

@app.errorhandler(404)
def page_not_found(e):
    flash("pagina no encontrada")
    return redirect("/")

@app.errorhandler(405)
def not_allow_page(e):
    flash("pagina no permitida")
    return redirect("/")



# manejar el login #
@app.route("/login-user", methods = ["POST"])
def login() -> None:
    # recuperamos la contraseña del formulario #
    password = request.form["password"]

    # verificamos que la contraseña sea la correcta #
    if password == os.getenv("APP_FACULTAD_PASSWORD"):
        session["logueado"] = True
        return redirect("/panel")
    else:
        flash("contraseña incorrecta")
        return redirect("/")
    
# crear materia
@app.route("/crear-materia", methods = ["POST"])
def crear_materia() -> None:
    # recuperamos los datos cargados en el formulario #
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    if not descripcion:
        descripcion = None
    carga = int(request.form["carga"])

    # creamos la tabla si es que no existe #
    db.crear_tabla()
    # agregamos la materia a la base de datos #
    db.insertar_materia(nombre,descripcion,carga)
    # volvemos a la pagina de crear la materia
    flash(f"se creo la materia {nombre}")
    return redirect("/cargar-materia")

@app.route("/ver-materias")
def get_ver_materias():
    if "logueado" in session:
        # obtenemos la lista con las materias
        listaMaterias = db.obtener_materias()
        return render_template("ver_materias.html",materias = listaMaterias)
    else:
        flash("no esta logueado")
        return redirect("/")
    






    









if __name__ == "__main__":
    app.run(debug=False)