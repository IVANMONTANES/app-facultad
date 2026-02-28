import sqlite3
from funciones.clases.clases import Materia



rutaDb = "db/base.db"

def crear_tabla_materias() -> None:
    with sqlite3.connect(rutaDb) as con:
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
    with sqlite3.connect(rutaDb) as con:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO materias (nombre,descripcion,carga_semanal) VALUES (?,?,?) 
        """,(nombre,descripcion,carga))
        con.commit()


def obtener_materia_por_id(id_materia: int) -> Materia:

    with sqlite3.connect(rutaDb) as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("""
            SELECT * FROM MATERIAS where id_materia = ?""",(id_materia,))
        
        fila = cursor.fetchone()

        # verificamos que se haya traido una fila #
        if fila is not None:
            materia_traida = Materia(fila["id_materia"],fila["nombre"],fila["descripcion"],fila["carga_semanal"])
            return materia_traida
        
        return fila



def obtener_materias():
    with sqlite3.connect(rutaDb) as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("""
            SELECT * FROM materias""")
        materias = cursor.fetchall()
        listaMaterias = [Materia(materiaFila["id_materia"],materiaFila["nombre"],materiaFila["descripcion"],materiaFila["carga_semanal"]) for materiaFila in materias]
        return listaMaterias
        



