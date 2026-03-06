from modulos.db import estudioDb,examenDb,horariosDb,materiasDb
import os

# creamos la carpeta database si no existe #
def crear_database():
    os.makedirs("database",exist_ok=True)

# funcion global que crea todas las tablas #
def crear_tablas() -> None:
    materiasDb.crear_tabla_materias()
    horariosDb.crear_tabla_horarios()
    estudioDb.crear_tabla_estudios()
    examenDb.crear_tabla_examenes()

    

            




    
        

        