from modulos import globales

class Horario:
    @staticmethod
    def obtener_dias(horarios: dict):

        # verificamos que haya horarios cargados #
        if horarios is None:
            return globales.horarios_no_cargados
        
        # recorremos el diccionario viendo que dias no estan cargados para agregar un texto informartivo #
        for dia, horario in horarios.items():
            if not horario:
                horarios[dia] = "No se cargo ningun horario"

        return horarios
    
    @staticmethod
    def actualizar_horarios(id_materia: int,diccionario_horarios:dict):
        from modulos.db import horariosDb


        horarios_materia = horariosDb.obtener_horario_materia(id_materia)

        # verificamos si ya hay horarios cargados para este materia #
        if horarios_materia:
            for dia,horario in diccionario_horarios.items():
                # verificamos si el horario esta vacio, si lo esta dejamos el horario anterior #
                if not horario:
                    diccionario_horarios[dia] = horarios_materia[dia]
        
        # actualizamos los horarios en la base de datos #
            horariosDb.modificar_horarios(diccionario_horarios,id_materia)
        # en el caso de no haber un horario cargado lo creamos #    
        else:
            horariosDb.insertar_horarios(diccionario_horarios,id_materia)