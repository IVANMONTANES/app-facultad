import sqlite3
from funciones.clases.clases import Examen

rutaDb = "db/base.db"

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
                FOREIGN KEY (id_materia) REFERENCES materias(id_materia)              
            )""")
        
def insertar_examen(id_materia: int, nombre: str, fecha: str, hora: str) -> None:
    with sqlite3.connect(rutaDb) as con:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO examenes (id_materia,nombre,fecha,hora) VALUES (?,?,?,?)
        """,(id_materia,nombre,fecha,hora))
        con.commit()

def obtener_examenes_por_id_materia(id_materia: int, estado_buscado:int) -> list[Examen]:
    with sqlite3.connect(rutaDb) as con:
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
    with sqlite3.connect(rutaDb) as con:
        cursor = con.cursor()
        cursor.execute("""
            UPDATE examenes set nota = ?, realizado = ? WHERE id_examen = ?""",(nota,nuevo_estado,id_examen))
        con.commit()