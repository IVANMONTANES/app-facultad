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



#-------------------- LOGIN -----------------------#


# FUNCION QUE VERIFICA SI LA CONTRASEÑA INGRESADA ES LA CORRECTA #
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
    


# FUNCION QUE SE ENCARGA, DE RECIBIR LOS DATOS DEL FORMULARIO, Y CREAR LA MATERIA EN LA BASE DE DATOS #
@app.route("/crear-materia", methods = ["POST"])
def crear_materia() -> None:
    # recuperamos los datos cargados en el formulario #
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    carga = int(request.form["carga"])

    # verificamos si la descripcion vino vacia #

    if not descripcion:
        descripcion = None

    # creamos la tabla si es que no existe #
    db.crear_tabla()

    # agregamos la materia a la base de datos #
    db.insertar_materia(nombre,descripcion,carga)

    # volvemos a la pagina de crear la materia
    flash(f"se creo la materia {nombre}")
    return redirect("/cargar-materia")

# FUNCION QUE SE ENCARGA DE OBTENER TODAS LAS MATERIAS DE LA BASE DE DATOS Y RENDERIZARLAS #
@app.route("/ver-materias")
def get_ver_materias():
    if "logueado" in session:
        # obtenemos la lista con las materias
        listaMaterias = db.obtener_materias()

        return render_template("ver_materias.html",materias = listaMaterias)
    else:
        flash("no esta logueado")
        return redirect("/")

    
@app.route("/materia/<int:id_materia>")
def get_materia(id_materia):
    if "logueado" in session:
        # obtenemos la materia por el id
        materia_con_id = db.obtener_materia_por_id(id_materia)
        return render_template("materia.html",materia = materia_con_id)
    else:
        flash("no esta logueado")
        return redirect("/")
    
# SECCION HORARIOS #
# -------------------------------------------------------------------- #
    
@app.route("/horarios/<int:id_materia>")
def get_horarios_page(id_materia):
    if "logueado" in session:
        # obtenemos la materia por el id
        materia_con_id = db.obtener_materia_por_id(id_materia)

        # verificamos que si haya traido una materia para que no se pueda acceder a materias no creadas #
        if materia_con_id is None:
            flash("no existe la materia ingresada")
            return redirect("/")

        # verificamos si ya tiene horarios cargados #
        horarios2 = db.obtener_horario_por_materia_id(id_materia)

        if horarios2 is None:
            horarios2 = {
                "Lunes": "No se cargo ningun horario",
                "Martes": "No se cargo ningun horario",
                "Miercoles": "No se cargo ningun horario",
                "Jueves": "No se cargo ningun horario",
                "Viernes": "No se cargo ningun horario",
                "Sabado": "No se cargo ningun horario",
                "Domingo": "No se cargo ningun horario",
            }
            return render_template("horarios.html",materia = materia_con_id, horarios = horarios2)
        else:
            # recorremos el diccionario viendo que dias no estan cargados para agregar un texto informartivo #
            for dia, horario in horarios2.items():
                if not horario:
                    horarios2[dia] = "no se cargo ningun horario"
            return render_template("horarios.html",materia = materia_con_id,horarios = horarios2)

    else:
        flash("no esta logueado")
        return redirect("/")
    
@app.route("/guardar-horarios", methods = ["POST"])
def save_horarios():
    # recibimos los datos traidos del formulario #
    id_materia = int(request.form["id_materia"])
    lunes = request.form["lunes"]
    martes = request.form["martes"]
    miercoles = request.form["miercoles"]
    jueves = request.form["jueves"]
    viernes = request.form["viernes"]
    sabado = request.form["sabado"]
    domingo = request.form["domingo"]

    # creamos un diccionario con los horarios pasados #
    diccionario_horarios = {
        "Lunes": lunes,
        "Martes":martes,
        "Miercoles":miercoles,
        "Jueves": jueves,
        "Viernes": viernes,
        "Sabado": sabado,
        "Domingo": domingo
        
    }
    
    
    horarios_materia = db.obtener_horario_por_materia_id(id_materia)
    # verificamos si ya hay horarios cargados para este materia #
    if horarios_materia:
        for dia,horario in diccionario_horarios.items():
            # verificamos si el horario esta vacio, si lo esta dejamos el horario anterior #
            if not horario:
                diccionario_horarios[dia] = horarios_materia[dia]
        
        # actualizamos los horarios en la base de datos #
        db.modificar_horarios(diccionario_horarios,id_materia)
    # en el caso de no haber un horario cargado lo creamos #    
    else:
        db.insertar_horarios(diccionario_horarios,id_materia)

    flash("horarios modificados con exito")
    return redirect(f"/horarios/{id_materia}")

# FIN SECCION HORARIOS #
# -------------------------------------------------------------------- #



# # SECCION EXAMENES #
# -------------------------------------------------------------------- #
@app.route("/examenes/<int:id_materia>")
def get_examenes_page(id_materia):
    if "logueado" in session:
        # obtenemos la materia con ese id #
        materia = db.obtener_materia_por_id(id_materia)

        # obtenemos los examenes pendientes de la materia #
        examenes_pendientes_materia = db.obtener_examenes_por_id_materia(id_materia,0)

        # obtenemos los examenes realizados de la materia #
        examenes_realizados_materia = db.obtener_examenes_por_id_materia(id_materia,1)

        # verificamos que si haya traido una materia para que no se pueda acceder a materias no creadas #
        if materia is None:
            flash("no existe la materia ingresada")
            return redirect("/")


        return render_template("examenes.html",materia = materia, examenes_pendientes = examenes_pendientes_materia, examenes_realizados = examenes_realizados_materia)
    else:
        flash("no esta logueado")
        return redirect("/")
    
@app.route("/crear-examen", methods = ["POST"])
def crear_examen() -> None:
    # obtenemos los datos cargados en el formulario #
    id_materia = int(request.form["id_materia"])
    nombre = request.form["nombre"]
    fecha = request.form["fecha"]
    hora = request.form["hora"]

    # insertamos el examen en la base de datos #
    db.insertar_examen(id_materia,nombre,fecha,hora)

    flash("examen agregado correctamente")
    return redirect(f"examenes/{id_materia}")

@app.route("/realizar-examen", methods = ["POST"])
def realizar_examen() -> None:
    # obtenemos los datos cargados en el formulario #
    id_examen = int(request.form["id_examen"])
    id_materia = int(request.form["id_materia"])
    nota = int(request.form["nota"])
    estado_actual = int(request.form["estado_actual"])

    # actualizamos el examen #
    db.actualizar_estado_examen_por_id(id_examen,nota,estado_actual)
    
    if estado_actual == 0:
        flash("se realizo el examen correctamente")
    else:
        flash("se marco el examen como pendiente correctamente")
    return redirect(f"examenes/{id_materia}")


@app.route("/marcar-examen-pendiente", methods = ["POST"])
def marcar_examen_pendiente() -> None:
    # obtenemos los datos cargados en el formulario #
    id_examen = int(request.form["id_examen"])
    id_materia = int(request.form["id_materia"])
    estado_actual = int(request.form["estado_actual"])

    # actualizamos el examen #
    db.actualizar_estado_examen_por_id(id_examen,None,estado_actual)

    if estado_actual == 0:
        flash("se realizo el examen correctamente")
    else:
        flash("se marco el examen como pendiente correctamente")
    return redirect(f"examenes/{id_materia}")


# # SECCION ESTUDIOS #
# -------------------------------------------------------------------- #
@app.route("/estudio/<int:id_materia>")
def get_estudio_page(id_materia):
    if "logueado" in session:
        # obtenemos la materia con ese id #
        materia = db.obtener_materia_por_id(id_materia)

        # verificamos que si haya traido una materia para que no se pueda acceder a materias no creadas #
        if materia is None:
            flash("no existe la materia ingresada")
            return redirect("/")
        
        return render_template("estudio.html",materia = materia)
    else:
        flash("no esta logueado")
        return redirect("/")
    







    
       

    
    






    









if __name__ == "__main__":
    db.crear_tabla_materias()
    db.crear_tabla_horarios()
    db.crear_tabla_examenes()
    app.run(debug=False) 