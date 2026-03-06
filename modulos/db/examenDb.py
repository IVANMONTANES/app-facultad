import sqlite3
from modulos.clases.examenes import Examen
from modulos import globales


rutaDb = globales.rutadb


def crear_tabla_examenes() -> None:
    with sqlite3.connect(rutaDb) as con:
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
                notificado_en DATETIME DEFAULT NULL,
                FOREIGN KEY (id_materia) REFERENCES materias(id_materia)              
            )""")
        
def insertar_examen(id_materia: int, nombre: str, fecha: str, hora: str) -> None:
    with sqlite3.connect(rutaDb) as con:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO examenes (id_materia,nombre,fecha,hora) VALUES (?,?,?,?)
        """,(id_materia,nombre,fecha,hora))
        con.commit()

def obtener_examenes_materia(id_materia: int, estado_buscado:int) -> list[Examen]:
    with sqlite3.connect(rutaDb) as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("""
            SELECT 
            id_examen,
            id_materia,nombre,
            fecha,
            hora,
            nota
            FROM examenes 
            WHERE id_materia = ? AND realizado = ?
            ORDER BY fecha ASC
        """,(id_materia,estado_buscado))
        
        # verificamos que se haya traido al menos un examen #
        filas = cursor.fetchall()
        
        examenes = [Examen(fila["id_examen"],fila["id_materia"],fila["nombre"],fila["fecha"],fila["hora"],fila["nota"]) for fila in filas]

        return examenes
    
def actualizar_estado_examen(id_examen: int,nota: int,estado_actual:int):
    nuevo_estado = 0 if estado_actual == 1 else 1
    with sqlite3.connect(rutaDb) as con:
        cursor = con.cursor()
        cursor.execute("""
            UPDATE examenes set nota = ?, realizado = ? WHERE id_examen = ?""",(nota,nuevo_estado,id_examen))
        con.commit()

def obtener_examenes_no_notificados() -> list[Examen]:
    """
    obtiene los examenes no notificados de hoy y mañana
    
    parametros:
        no recibe

    comportamiento:
        - ejecuta la consulta sql, que obtiene que los examenes no notificados ordenadas de mas proximo a menos proximo
        - crea una lista por compresion de objetos de tipo examen

    retorna:
        List[Examen]: la lista de examenes no notificados

    """
    with sqlite3.connect(rutaDb) as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("""
            SELECT id_examen,id_materia, nombre, fecha, hora, nota 
            FROM examenes 
            WHERE notificado_en IS NULL
            AND date(fecha) IN ( date('now'),date('now','+1 day') )
            ORDER BY fecha ASC, hora ASC
        """)
        filas = cursor.fetchall()

        examenes_no_notificados = [Examen(fila["id_examen"],fila["id_materia"],fila["nombre"],fila["fecha"],fila["hora"],fila["nota"]) for fila in filas]

        return examenes_no_notificados
    

def marcar_examen_como_notificado(id_examen:int) -> None:
    """
    marca un examen como ya notificado

    parametros:
        id_examen (int): id del examen que sera marcado

    comportamiento:
        - ejecuta la consulta sql que marca el examen como notificado a la hora actual
    
    retorna:
        None: no retorna nada
    
    """
    from datetime import datetime
    with sqlite3.connect(rutaDb) as con:
        cursor = con.cursor()
        cursor.execute("""
            update examenes
            SET notificado_en = ?
            WHERE id_examen = ?
        """,(datetime.now().isoformat(),id_examen))

def eliminar_examen(id_examen: int) -> None:
    """
    funcion que se encarga de eliminar un examen en concreto

    parametros:
        id_examen (int): id de el examen

    comportamiento:
        - ejecuta la consulta sql que se encarga de eliminar el examen con ese id

    retorna:
        None: no retorna nada

    """
    with sqlite3.connect(rutaDb) as con:
        cursor = con.cursor()
        cursor.execute("""
            DELETE FROM examenes
            WHERE id_examen = ?
        """,(id_examen,))

def eliminar_examenes_materia(id_materia: int) -> None:
    """
    funcion que se encarga de eliminar todos los examenes de una materia

    parametros:
        id_materia (int): id de la materia

    comportamiento:
        - ejecuta la consulta sql que se encarga de eliminar todos los examenes de la materia

    retorna:
        None: no retorna nada

    """
    with sqlite3.connect(rutaDb) as con:
        cursor = con.cursor()
        cursor.execute("""
            DELETE FROM examenes
            WHERE id_materia = ?
        """,(id_materia,))