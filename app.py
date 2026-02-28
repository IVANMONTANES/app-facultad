# dependencias de flask #
from flask import Flask, render_template, request, flash, redirect, session,Response

# dependencias para manejar las rutas ""
import os

# dependencias de la base de datos #
from funciones.db import materiasDb,horariosDb,examenDb,estudioDb,dbBase

# dependencias de las clases #
from funciones.clases.clases import Materia,Estudio,Examen,Fecha,Horario

# dependencias para manejar las fechas #
from datetime import datetime

# dependencias de variables globales #
from funciones import globales



app = Flask(__name__)
app.secret_key = "clave_super_secreta"

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# ------------------------ FUNCIONES DE DIRECCIONAMIENTO ------------------------------ #


@app.route("/")
def get_index_page() -> Response:
    """

    gestiona el ingreso a la ruta raiz del proyecto.

    parametros:
        no recibe parametros
    
    comportamiento:
        - si el usuario esta logueado:
            - redirige hacia /panel
        - si el usuario no esta logueado:
            - redirige hacia /login
    
    retorna:
        Response: un objeto Response de redireccionamiento 

    """


    if "logueado" in session:
        return redirect("/panel")
    
    return redirect("/login")
    

@app.route("/login")
def get_login_page() -> Response:
    """

    gestiona el ingreso a la ruta /login

    parametros:
        no recibe
    
    comportamiento:
        - si el usuario esta logueado:
            - redirige hacia /panel
        - si el usuario no esta logueado:
            - renderiza login.html

    retorna: 
        Response: si esta logueado, una respuesta de redireccionamiento, si no una respuesta de renderizado

    """

    if "logueado" in session:
        flash("ya esta logueado")
        return redirect("/panel")
    
    return render_template("login.html")
   


@app.route("/panel")
def get_panel_page() -> Response:
    """

    gestiona el ingreso a la ruta /panel del proyecto

    parametros:
        no recibe
    
    comportamiento:
        - si el usuario esta logueado:
            - renderiza panel.html
        - si el usuario no esta logueado:
            - redirige hacia /login
    
    retorna:
        Response: si el usuario esta logueado, una response de renderizado, si no una response de redireccionamiento

    """

    if "logueado" in session:
        return render_template("panel.html")
    
    flash("debe loguearse primero")
    return redirect("/login")
    

@app.route("/cargar-materia")
def get_cargar_materia_page() -> Response:
    """
    
    gestiona el ingreso a la ruta /cargar-materia del proyecto

    parametros:
        no recibe
    
    comportamiento:
        - si el usuario esta logueado:
            - renderiza cargar_materia.html
        - si el usuario no esta logueado:
            - redirige hacia /login
    
    retorna:
        Response: si el usuario esta logueado, una response de renderizado, si no una response de redireccionamiento

    """

    if "logueado" in session:
        return render_template("cargar_materia.html")
    
    flash("no esta logueado")
    return redirect("/login")


@app.route("/ver-materias")
def get_ver_materias_page() -> Response:
    """
    
    gestiona el ingreso a la ruta /ver-materia del proyecto

    parametros:
        no recibe

    comportamiento:
        - si el usuario esta logueado:
            - obtiene la lista de materias de la base datos
            - renderiza ver_materias.html con la lista de materias
        - si el usuario no esta logueado:
            - redirige hacia /login
    
    retorna:
        Response: si el usuario esta logueado, una response de renderizado, si no una response de redireccionamiento

    """

    if "logueado" in session:
        # obtenemos la lista con las materias #
        listaMaterias = materiasDb.obtener_materias()
        return render_template("ver_materias.html",materias = listaMaterias)
    
    flash("no esta logueado")
    return redirect("/login")
    

@app.route("/materia/<int:id_materia>")
def get_materia_page(id_materia: int) -> Response:
    """

    gestiona el acceso a la ruta /materia/id_materia del proyecto

    parametros:
        id_materia (int): id de la materia que se mostrara

    comportamiento:
        - si el usuario esta logueado:
            - se busca la materia en la base de datos.
            - si existe: se renderiza materia.html.
            - si no existe: redirige hacia /panel
        - si el usuario no esta logueado:
            - redirige hacia /login
    
    retorna:
        Response: de redireccionamiento o de renderizado segun el flujo
        
    """

    if "logueado" in session:
        # obtenemos la materia por el id
        materia = materiasDb.obtener_materia_por_id(id_materia)

        # verificamos que se haya traido una materia #
        if materia:
            return render_template("materia.html",materia = materia)
        
        flash("materia no encontrada")
        return redirect("/panel")
    
    flash("no esta logueado")
    return redirect("/login")
    
@app.route("/horarios/<int:id_materia>")
def get_horarios_page(id_materia) -> Response:
    """
    gestiona el acceso a la ruta /horarios/id_materia del proyecto

    parametros:
        id_materia (int): id de la materia que se mostrara
    
    comportamiento:
        - si el usuario esta logueado:
            - se busca la materia en la base de datos
            - si la materia no existe redirige hacia /panel
            - si la materia existe se buscan los horarios de la materia
            - se llama a la funcion obtener_dias que se encarga de gestionar como se mostraran los horarios
            - se renderiza horarios.html con la materia y los horarios
        - si el usuario no esta logueado:
            - se redirige hacia /login

    retorna:
        Response: de redireccionamiento o de renderizado segun el flujo
    
    """
    if "logueado" in session:
        # obtenemos la materia por el id #
        materia = materiasDb.obtener_materia_por_id(id_materia)

        # verificamos que si haya traido una materia para que no se pueda acceder a materias no creadas #
        if materia is None:
            flash("no existe la materia ingresada")
            return redirect("/panel")

        # traemos los horarios de la materia de la base de datos #
        horarios_traidos = horariosDb.obtener_horario_por_id_materia(id_materia)

        # funcion que se encarga de devolver el diccionario bien cargado #
        horarios = Horario.obtener_dias(horarios_traidos)

        return render_template("horarios.html",materia = materia,horarios = horarios)

    flash("no esta logueado")
    return redirect("/login")



@app.route("/examenes/<int:id_materia>")
def get_examenes_page(id_materia) -> Response:
    """

    gestiona el acceso a la ruta /examenes/id_materia del proyecto

    parametros:
        id_materia (int): id de la materia que se mostrara

    comportamiento:
        - si el usuario esta logueado:
            - se busca la materia en la base de datos
            - si la materia no existe redirige hacia /panel
            - si la materia existe, se obtienen los examenes pendienes y realizados usando las funciones definidas en examenDb
            - se renderiza examenes.html con la materia, los examanes pendientes y los realizados
        - si el usuario no esta logueado:
            - redirige hacia /login

    retorna:
        Response: de redireccionamiento o de renderizado segun el flujo
    
    """

    if "logueado" in session:
        # obtenemos la materia con ese id #
        materia = materiasDb.obtener_materia_por_id(id_materia)

        # verificamos que si haya traido una materia para que no se pueda acceder a materias no creadas #
        if materia is None:
            flash("no existe la materia ingresada")
            return redirect("/panel")
        
        # obtenemos los examenes pendientes de la materia #
        examenes_pendientes_materia = examenDb.obtener_examenes_por_id_materia(id_materia,0)

        # obtenemos los examenes realizados de la materia #
        examenes_realizados_materia = examenDb.obtener_examenes_por_id_materia(id_materia,1)

        
        return render_template("examenes.html",materia = materia, examenes_pendientes = examenes_pendientes_materia, examenes_realizados = examenes_realizados_materia)
    
    flash("no esta logueado")
    return redirect("/login")
    

    
@app.route("/estudio/<int:id_materia>")
def get_estudio_page(id_materia) -> Response:
    """
    gestiona el ingreso a la ruta /estudio/id_materia del proyecto

    parametros:
        id_materia (int): id de la materia que se mostrara
    
    comportamiento:
        - si el usuario esta logueado
            - se busca la materia en la base de datos
            - si la materia no existe se redirige hacia /panel
            - si la materia existe se llama a las funcion obtener_diccionario_ultima_semana que se encarga de devolver un diccionario con clave el dia y valor los minutos estudiados ese dia
            - se llama a la funcion calcular_media que suma los minutos estudiados toda la semana
            - se renderiza estudio.html con materia, el diccionario y la media
        - si el usuario no esta logueado
            - se redirige hacia /login
    
    retorna:
        Response: de redireccionamiento o de renderizado segun el flujo
    """

    if "logueado" in session:
        # obtenemos la materia con ese id #
        materia = materiasDb.obtener_materia_por_id(id_materia)

        # verificamos que si haya traido una materia para que no se pueda acceder a materias no creadas #
        if materia is None:
            flash("no existe la materia ingresada")
            return redirect("/panel")

        # funcion que se encarga de devolver un diccionario con el dia y los minutos totales que se estudio ese dia #
        diccionario = Estudio.obtener_diccionario_ultima_semana(id_materia)


        # funcion que se encarga de calcular la media de la semana #
        media = Estudio.calcular_media(diccionario)
        
        
        return render_template("estudio.html",materia = materia,diccionario_semana = diccionario, media = media)
    

    flash("no esta logueado")
    return redirect("/login")
    
# ------------------------ FIN FUNCIONES DE DIRECCIONAMIENTO ------------------------------ #

        

# ------------------------ FUNCIONES ASOCIADAS A VOLVER ------------------------------ #

@app.route("/volver-panel")
def volver_al_panel() -> None:
    return redirect("/panel")

@app.route("/volver-ver-materias")
def volver_a_ver_materias() -> None:
    return redirect("/ver-materias")

@app.route("/volver-materia/<int:id_materia>")
def volver_a_materia(id_materia) -> None:
    return redirect(f"/materia/{id_materia}")

# ------------------------ FIN FUNCIONES ASOCIADAS A VOLVER ------------------------------ #


# ------------------------ FUNCIONES ASOCIADAS A MANEJAR RUTAS PROBLEMATICAS ------------------------------  #

@app.errorhandler(404)
def page_not_found(e):
    flash("pagina no encontrada")
    return redirect("/")

@app.errorhandler(405)
def not_allow_page(e):
    flash("pagina no permitida")
    return redirect("/")

# ------------------------ FIN FUNCIONES ASOCIADAS A MANEJAR RUTAS PROBLEMATICAS ------------------------------  #




#-------------------- FUNCIONES QUE PROCESAN DATOS -----------------------#

# ---------- LOGIN ------------ #

# FUNCION QUE VERIFICA SI LA CONTRASEÑA INGRESADA ES LA CORRECTA #
@app.route("/login-user", methods = ["POST"])
def login() -> Response:
    """
    verifica si la contraseña ingresada es la misma que la guardada en el sistema

    parametros:
        no recibe
    
    comportamiento:
        - si la contraseña es igual:
            - se establece la sesion
            - se redirige hacia /panel
        - si la contraseña no es igual:
            - se redirige hacia /login

    retorna:
        Response: una response de redireccionamiento
    
    """
    # recuperamos la contraseña del formulario #
    password = request.form["password"]

    # verificamos que la contraseña sea la correcta #
    if password == os.getenv("APP_FACULTAD_PASSWORD"):
        session["logueado"] = True
        return redirect("/panel")
    else:
        flash("contraseña incorrecta")
        return redirect("/login")

# ------------ FIN LOGIN ----------- #




# ---------- MATERIAS ------------ #
@app.route("/crear-materia", methods = ["POST"])
def crear_materia() -> Response:
    """
    gestiona la insercion de una materia a la base de datos

    parametros:
        no recibe
    
    comportamiento:
        - recupera los datos cargados por el usuario
        - verifica si la descripcion vino vacia, para poder ponerle como null en la base de datos luego
        - usa la funcion insertar_materia que se encarga de insertar la materia en la base de datos
        - redirige haciaa /cargar-materia
    
    retorna:
        Response: una response de redireccionamiento
    
    """
    # recuperamos los datos cargados en el formulario #
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    carga = int(request.form["carga"])

    # verificamos si la descripcion vino vacia #

    if not descripcion:
        descripcion = None

    # agregamos la materia a la base de datos #
    materiasDb.insertar_materia(nombre,descripcion,carga)

    # volvemos a la pagina de crear la materia
    flash(f"se creo la materia {nombre}")
    return redirect("/cargar-materia")

# ------------ FIN MATERIAS --------------#


# ---------- HORARIOS ------------ #

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
    
    
    horarios_materia = horariosDb.obtener_horario_por_id_materia(id_materia)
    # verificamos si ya hay horarios cargados para este materia #
    if horarios_materia:
        for dia,horario in diccionario_horarios.items():
            # verificamos si el horario esta vacio, si lo esta dejamos el horario anterior #
            if not horario:
                diccionario_horarios[dia] = horarios_materia[dia]
        
        # actualizamos los horarios en la base de datos #
        horariosDb.modificar_horarios(diccionario_horarios,id_materia)
    # en el caso de no haber un horario cargado lo creamos #    
    else:
        horariosDb.insertar_horarios(diccionario_horarios,id_materia)

    flash("horarios modificados con exito")
    return redirect(f"/horarios/{id_materia}")

# ----------- FIN HORARIOS ------------ #

# ------------- ESTUDIO --------------- #

@app.route("/guardar-estudio", methods = ["POST"])
def guardar_estudio() -> None:
    # obtenemos los datos cargados en el formulario #
    id_materia = int(request.form["id_materia"])
    horas_estudio = int(request.form["horas_estudio"])
    fecha = request.form["fecha"]

    print(f"fecha guardada {fecha}")

    # insertamos el estudio en la base de datos #
    estudioDb.insertar_estudio(id_materia,horas_estudio,fecha)

    flash("dia de estudio agregado correctamente")
    return redirect(f"/estudio/{id_materia}")

# ------------- FIN ESTUDIO ------------- #


# ------------ EXAMEN ---------------- #

@app.route("/crear-examen", methods = ["POST"])
def crear_examen() -> None:
    # obtenemos los datos cargados en el formulario #
    id_materia = int(request.form["id_materia"])
    nombre = request.form["nombre"]
    fecha = request.form["fecha"]
    hora = request.form["hora"]

    # insertamos el examen en la base de datos #
    examenDb.insertar_examen(id_materia,nombre,fecha,hora)

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
    examenDb.actualizar_estado_examen_por_id(id_examen,nota,estado_actual)
    
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
    examenDb.actualizar_estado_examen_por_id(id_examen,None,estado_actual)

    if estado_actual == 0:
        flash("se realizo el examen correctamente")
    else:
        flash("se marco el examen como pendiente correctamente")
    return redirect(f"examenes/{id_materia}")

# ------------- FIN EXAMEN ------------- #

#-------------------- FIN FUNCIONES QUE PROCESAN DATOS -----------------------#










    
       

    
    






    









if __name__ == "__main__":
    dbBase.crear_tablas()
    app.run(debug=False) 