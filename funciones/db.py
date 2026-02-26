import sqlite3
from funciones.materia import Materia
from funciones.examen import Examen



# base de datos relacionado con la materia #
rutaMaterias = "db/materias.db"

def crear_tabla_materias() -> None:
    with sqlite3.connect(rutaMaterias) as con:
        cursor = con.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS materias (
                id_materia INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                carga_semanal INTEGER NOT NULL               
                       )
        """)

def insertar_materia(nombre: str, descripcion: str, carga: int) -> None:
    with sqlite3.connect(rutaMaterias) as con:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO materias (nombre,descripcion,carga_semanal) VALUES (?,?,?) 
""",(nombre,descripcion,carga))
        con.commit()

def obtener_materia_por_id(id: int) -> Materia:

    with sqlite3.connect(rutaMaterias) as con:
        cursor = con.cursor()
        cursor.execute("""
            SELECT * FROM MATERIAS where id_materia = ?""",(id,))
        materiaTupla = cursor.fetchone()
        
        if materiaTupla is None:
            return None
        
        # desempaquetado de la tupla #
        materia_id,materia_nombre,materia_descripcion,materia_carga = materiaTupla

        # instanciamos la materia #
        materia_traida = Materia(materia_id,materia_nombre,materia_descripcion,materia_carga)

        # retornamos la materia #
        return materia_traida

def obtener_materias():
    with sqlite3.connect(rutaMaterias) as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("""
            SELECT * FROM materias""")
        materias = cursor.fetchall()
        listaMaterias = [Materia(materiaFila["id_materia"],materiaFila["nombre"],materiaFila["descripcion"],materiaFila["carga_semanal"]) for materiaFila in materias]
        return listaMaterias
    

# base de datos relacionado con los horarios #
rutaHorarios = "db/horarios.db"


def crear_tabla_horarios() -> None:
    with sqlite3.connect(rutaHorarios) as con:
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

    with sqlite3.connect(rutaHorarios) as con:
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

    with sqlite3.connect(rutaHorarios) as con:
        cursor = con.cursor()
        cursor.execute("""
            UPDATE horarios SET lunes = ?, martes = ?, miercoles = ?, jueves = ?, viernes = ?, sabado = ?, domingo = ? WHERE id_materia = ?""",(lunes,martes,miercoles,jueves,viernes,sabado,domingo,id_materia))
        con.commit()

def obtener_horario_por_materia_id(id_materia: int) -> dict:
    with sqlite3.connect(rutaHorarios) as con:
        con.row_factory = sqlite3.Row

        cursor = con.cursor()
        cursor.execute("""
            SELECT lunes,martes,miercoles,jueves,viernes,sabado,domingo FROM horarios WHERE id_materia = ?""",(id_materia,))
        
        # obtenemos la fila #
        horarioFila = cursor.fetchone()

        # verificamos que haya traido un horario #
        if horarioFila is None:
            return None
        
        # creamos el diccionario #
        diccionario = {
            "Lunes": horarioFila["lunes"],
            "Martes": horarioFila["martes"],
            "Miercoles": horarioFila["miercoles"],
            "Jueves": horarioFila["jueves"],
            "Viernes": horarioFila["viernes"],
            "Sabado": horarioFila["sabado"],
            "Domingo": horarioFila["domingo"]    
        }

        return diccionario
    

# base de datos relacionada con examenes #
rutaExamenes = "db/examenes.db"


def crear_tabla_examenes() -> None:
    with sqlite3.connect(rutaExamenes) as con:
        cursor = con.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS examenes(
                id_examen INTEGER PRIMARY KEY AUTOINCREMENT,
                id_materia INTEGER NOT NULL,
                nombre TEXT NOT NULL,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL,
                nota INTEGER,
                realizado INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (id_materia) REFERENCES materias(id_materia)              
            )""")
        
def insertar_examen(id_materia: int, nombre: str, fecha: str, hora: str) -> None:
    with sqlite3.connect(rutaExamenes) as con:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO examenes (id_materia,nombre,fecha,hora) VALUES (?,?,?,?)
        """,(id_materia,nombre,fecha,hora))
        con.commit()

def obtener_examenes_por_id_materia(id_materia: int, estado_buscado:int) -> list[Examen]:
    with sqlite3.connect(rutaExamenes) as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("""
            SELECT id_examen ,nombre, fecha, hora, nota FROM examenes WHERE id_materia = ? AND realizado = ?
        """,(id_materia,estado_buscado))
        
        # verificamos que se haya traido al menos un examen #
        filas = cursor.fetchall()
        examenes = [Examen(fila["id_examen"],fila["nombre"],fila["fecha"],fila["hora"],fila["nota"]) for fila in filas]

        return examenes
    
def actualizar_estado_examen_por_id(id_examen: int,nota: int,estado_actual:int):
    nuevo_estado = 0 if estado_actual == 1 else 1
    with sqlite3.connect(rutaExamenes) as con:
        cursor = con.cursor()
        cursor.execute("""
            UPDATE examenes set nota = ?, realizado = ?""",(nota,nuevo_estado))
        con.commit()
        


    

            




    
        

        