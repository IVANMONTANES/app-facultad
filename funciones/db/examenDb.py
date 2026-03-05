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
            SELECT id_examen ,nombre, fecha, hora, nota FROM examenes WHERE id_materia = ? AND realizado = ?
        """,(id_materia,estado_buscado))
        
        # verificamos que se haya traido al menos un examen #
        filas = cursor.fetchall()
        examenes = [Examen(fila["id_examen"],fila["nombre"],fila["fecha"],fila["hora"],fila["nota"]) for fila in filas]

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
    Obtiene exámenes pendientes no notificados que ocurren mañana
    
    Retorna:
        list[Examen]: Lista de exámenes (vacía si no hay ninguno)



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
    from datetime import datetime
    with sqlite3.connect(rutaDb) as con:
        cursor = con.cursor()
        cursor.execute("""
            update examenes
            SET notificado_en = ?
            WHERE id_examen = ?
        """,(datetime.now().isoformat(),id_examen))