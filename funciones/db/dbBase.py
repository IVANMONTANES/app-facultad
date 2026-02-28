from funciones.db import estudioDb,examenDb,horariosDb,materiasDb

# funcion global que crea todas las tablas #
def crear_tablas() -> None:
    materiasDb.crear_tabla_materias()
    horariosDb.crear_tabla_horarios()
    estudioDb.crear_tabla_estudios()
    examenDb.crear_tabla_examenes()

    

            




    
        

        