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

def obtener_materia_por_id(id: int) -> Materia:
    with sqlite3.connect(ruta) as con:
        cursor = con.cursor()
        cursor.execute("""
            SELECT * FROM MATERIAS where id_materia = ?

""",(id,))
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
    with sqlite3.connect(ruta) as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("""
            SELECT * FROM materias""")
        materias = cursor.fetchall()
        listaMaterias = [Materia(materiaFila["id_materia"],materiaFila["nombre"],materiaFila["descripcion"],materiaFila["carga_semanal"]) for materiaFila in materias]
        return listaMaterias
    
        

        