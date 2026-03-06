from modulos import globales
from modulos.db import horariosDb

class Horarios:
    def __init__(self,id_horario: int,id_materia: int,lunes: str, martes: str, miercoles: str, jueves: str, viernes: str, sabado: str, domingo: str):
        self.id_horario = id_horario
        self.id_materia = id_materia
        self.lunes = lunes
        self.martes = martes
        self.miercoles = miercoles
        self.jueves = jueves
        self.viernes = viernes
        self.sabado = sabado
        self.domingo = domingo



    @staticmethod
    def obtener_dias(horarios: Horarios) -> dict:

        # verificamos que haya horarios cargados #
        if horarios is None:
            return globales.horarios_no_cargados
        
        # creamos un diccionario con los dias y sus horarios correspondientes #
        horarios_diccionario = {
            "lunes": horarios.lunes,
            "martes": horarios.martes,
            "miercoles": horarios.miercoles,
            "jueves": horarios.jueves,
            "viernes": horarios.viernes,
            "sabado": horarios.sabado,
            "domingo": horarios.domingo
        }


        
        # recorremos el diccionario viendo que dias no estan cargados para agregar un texto informativo #
        for dia, horario in horarios_diccionario.items():
            if not horario:
                horarios_diccionario[dia] = "No se cargo ningun horario"

        return horarios_diccionario
    
    @staticmethod
    def actualizar_horarios(id_materia: int,diccionario_horarios:dict):

        horarios = horariosDb.obtener_horarios_materia(id_materia)

        # verificamos si ya hay horarios cargados para este materia #
        if horarios:
            # creamos un diccionario con los dias y sus horarios correspondientes #
            horarios_diccionario = {
                "Lunes": horarios.lunes,
                "Martes": horarios.martes,
                "Miercoles": horarios.miercoles,
                "Jueves": horarios.jueves,
                "Viernes": horarios.viernes,
                "Sabado": horarios.sabado,
                "Domingo": horarios.domingo
            }

            for dia,horario in diccionario_horarios.items():
                # verificamos si el horario esta vacio, si lo esta dejamos el horario anterior #
                if not horario:
                    diccionario_horarios[dia] = horarios_diccionario[dia]
        
        # actualizamos los horarios en la base de datos #
            horariosDb.modificar_horarios(diccionario_horarios,id_materia)
           
        else:
            horariosDb.insertar_horarios(diccionario_horarios,id_materia)