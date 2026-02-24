from flask import Flask, render_template, request, flash, redirect, session
import os

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
    return render_template("panel.html")

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
    









if __name__ == "__main__":
    app.run(debug=False)