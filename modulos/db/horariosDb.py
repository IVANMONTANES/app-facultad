import sqlite3
from modulos.clases.horarios import Horarios
from modulos import globales

rutaDb = globales.rutadb


def crear_tabla_horarios() -> None:
    with sqlite3.connect(rutaDb) as con:
        cursor = con.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS horarios (
                id_horario INTEGER PRIMARY KEY,
                id_materia INTEGER NOT NULL,
                lunes TEXT,
                martes TEXT,
                miercoles TEXT,
                jueves TEXT,
                viernes TEXT,
                sabado TEXT,
                domingo TEXT,
                FOREIGN KEY (id_materia) REFERENCES materias(id_materia)                             
                       )""")
        
def insertar_horarios(horarios: dict,id_materia: int) -> None:

    # obtenemos los horarios de cada dia del diccionario #
    lunes = horarios["Lunes"]
    martes = horarios["Martes"]
    miercoles = horarios["Miercoles"]
    jueves = horarios["Jueves"]
    viernes = horarios["Viernes"]
    sabado = horarios["Sabado"]
    domingo = horarios["Domingo"]

    with sqlite3.connect(rutaDb) as con:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO horarios (id_materia,lunes,martes,miercoles,jueves,viernes,sabado,domingo) VALUES (?,?,?,?,?,?,?,?)""",(id_materia,lunes,martes,miercoles,jueves,viernes,sabado,domingo))
        con.commit()

def modificar_horarios(horarios: dict, id_materia: int) -> None:

    # obtenemos los horarios de cada dia del diccionario #
    lunes = horarios["Lunes"]
    martes = horarios["Martes"]
    miercoles = horarios["Miercoles"]
    jueves = horarios["Jueves"]
    viernes = horarios["Viernes"]
    sabado = horarios["Sabado"]
    domingo = horarios["Domingo"]

    with sqlite3.connect(rutaDb) as con:
        cursor = con.cursor()
        cursor.execute("""
            UPDATE horarios SET 
            lunes = ?, 
            martes = ?, 
            miercoles = ?, 
            jueves = ?, 
            viernes = ?, 
            sabado = ?, 
            domingo = ? 
            WHERE id_materia = ?""",(lunes,martes,miercoles,jueves,viernes,sabado,domingo,id_materia))
        con.commit()


def obtener_horarios_materia(id_materia: int) -> Horarios:
    with sqlite3.connect(rutaDb) as con:
        con.row_factory = sqlite3.Row

        cursor = con.cursor()
        cursor.execute("""
            SELECT * FROM horarios 
            WHERE id_materia = ?""",(id_materia,))
        
        # obtenemos la fila #
        fila = cursor.fetchone()

        # verificamos que haya traido un horario #
        if fila is None:
            return None
        
        # creamos el horario #
        horarios = Horarios(fila["id_horario"],fila["id_materia"],fila["lunes"],fila["martes"],fila["miercoles"],fila["jueves"],fila["viernes"],fila["sabado"],fila["domingo"])

        return horarios
    
def eliminar_horarios_materia(id_materia: int) -> None:
    """
    funcion que se encarga de eliminar todos los horarios de una materia

    parametros:
        id_materia (int): id de la materia

    comportamiento:
        - ejecuta la consulta sql que se encarga de eliminar todos los horarios de la materia

    retorna:
        None: no retorna nada
        
    """
    with sqlite3.connect(rutaDb) as con:
        cursor = con.cursor()
        cursor.execute("""
            DELETE FROM horarios
            WHERE id_materia = ?
        """,(id_materia,))

def eliminar_dia(id_horario: int, dia: str):
    with sqlite3.connect(rutaDb) as con:
        cursor = con.cursor()
        cursor.execute(f"""
            UPDATE horarios set
            {dia} = ?
            WHERE id_horario = ?
        """,("No se cargo ningun horario",id_horario))