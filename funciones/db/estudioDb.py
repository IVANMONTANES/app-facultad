import sqlite3
from funciones.clases.clases import Estudio

rutaDb = "db/base.db"


def crear_tabla_estudios() -> None:
    with sqlite3.connect(rutaDb) as con:
        cursor = con.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estudios(
                id_estudio INTEGER PRIMARY KEY AUTOINCREMENT,
                id_materia INTEGER NOT NULL,
                horas_estudio INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                FOREIGN KEY (id_materia) REFERENCES materias(id_materia)              
            )""")
        
def insertar_estudio(id_materia: int,horas_estudio: int, fecha: str) -> None:
    with sqlite3.connect(rutaDb) as con:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO estudios (id_materia,horas_estudio,fecha) VALUES (?,?,?)
        """,(id_materia,horas_estudio,fecha))
        con.commit()

def obtener_estudios_por_id_materia(id_materia: int) -> list[Estudio]:
    with sqlite3.connect(rutaDb) as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("""
            SELECT id_estudio, horas_estudio, fecha FROM estudios WHERE id_materia = ?
        """,(id_materia,))
        
        # verificamos que se haya traido al menos un estudio #
        filas = cursor.fetchall()
        estudios = [Estudio(fila["id_estudio"],fila["horas_estudio"],fila["fecha"]) for fila in filas]

        return estudios

def obtener_estudio_por_id_materia_ordenados(id_materia: int) -> list[Estudio]:
    with sqlite3.connect(rutaDb) as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("""
            SELECT id_estudio, horas_estudio, fecha FROM estudios WHERE id_materia = ? ORDER BY fecha DESC """,(id_materia,))
        
        filas = cursor.fetchall()
        estudios_ordenados = [Estudio(fila["id_estudio"],fila["horas_estudio"],fila["fecha"]) for fila in filas]
        return estudios_ordenados
    
def obtener_estudios_por_fecha(id_materia:int, fecha: str) -> list[Estudio]:
    with sqlite3.connect(rutaDb) as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("""
            SELECT id_estudio, horas_estudio, fecha from estudios WHERE id_materia = ? AND fecha = ?""",(id_materia,fecha))

        filas = cursor.fetchall()
        estudios_fecha = [Estudio(fila["id_estudio"],fila["horas_estudio"],fila["fecha"]) for fila in filas]
        return estudios_fecha