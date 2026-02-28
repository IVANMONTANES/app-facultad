import sqlite3


rutaDb = "db/base.db"

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
            UPDATE horarios SET lunes = ?, martes = ?, miercoles = ?, jueves = ?, viernes = ?, sabado = ?, domingo = ? WHERE id_materia = ?""",(lunes,martes,miercoles,jueves,viernes,sabado,domingo,id_materia))
        con.commit()


def obtener_horario_por_id_materia(id_materia: int) -> dict:
    with sqlite3.connect(rutaDb) as con:
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
