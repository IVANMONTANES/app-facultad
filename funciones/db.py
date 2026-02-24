import sqlite3
from funciones.materia import Materia

ruta = "db/materias.db"

def crear_tabla() -> None:
    with sqlite3.connect(ruta) as con:
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
    with sqlite3.connect(ruta) as con:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO materias (nombre,descripcion,carga_semanal) VALUES (?,?,?) 
""",(nombre,descripcion,carga))
        con.commit()

def obtener_materias():
    with sqlite3.connect(ruta) as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("""
            SELECT nombre,descripcion,carga_semanal FROM materias""")
        materias = cursor.fetchall()

        listaMaterias = [Materia(materiaFila["nombre"],materiaFila["descripcion"],materiaFila["carga_semanal"]) for materiaFila in materias]
        return listaMaterias
    
        

        