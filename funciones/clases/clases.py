from datetime import date,timedelta
import locale
from funciones import globales

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# ------------------ CLASE MATERIA ---------------------- #
class Materia:
    def __init__(self,id_materia,nombre: str,descripcion: str, carga: int):
        self.id_materia = id_materia
        self.nombre = nombre
        self.descripcion = descripcion
        self.carga = carga

# ------------------ CLASE HORARIO ---------------------- #
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
        from funciones.db import horariosDb


        horarios_materia = horariosDb.obtener_horario_por_id_materia(id_materia)

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


# ------------------ CLASE ESTUDIO ---------------------- #
class Estudio:
    def __init__(self,id_estudio:int ,horas_estudio:int, fecha: str):
        self.id_estudio = id_estudio
        self.horas_estudio = horas_estudio
        self.fecha = fecha

    @staticmethod
    def sumar_horas_estudio(estudios: list[Estudio]):
        total_horas = 0
        for estudio in estudios:
            total_horas += estudio.horas_estudio
        return total_horas
    
    @staticmethod
    def obtener_diccionario_ultima_semana(id_materia: int):
        from funciones.db import estudioDb
        # obtenemos la ultima semana #
        ultima_semana = Fecha.obtener_ultima_semana()

        # diccionario por compresion, que carga el dia y las horas estudiadas ese dia #

        diccionario = {dia.strftime("%d De %B De %Y"): Estudio.sumar_horas_estudio(estudioDb.obtener_estudios_por_fecha(id_materia,dia)) for dia in ultima_semana}

        return diccionario

    @staticmethod
    def calcular_media(diccionario: dict):
        media = 0
        
        for horas in diccionario.values():
            media += horas

        return media
        

    
    



# ------------------ CLASE EXAMEN ---------------------- #
class Examen:
    def __init__(self,id_examen:int ,nombre:str, fecha: str, hora: str, nota: int):
        self.id_examen = id_examen
        self.nombre = nombre
        self.fecha = fecha
        self.hora = hora
        self.nota = nota





# ------------------ FUNCIONES FECHA ----------------------- #
# vamos a usar una clase con metodos estaticos en vez de funciones sueltas #
class Fecha:
    @staticmethod
    def obtener_ultima_semana() -> list[date]:
        # obtenemos la fecha actual #
        fecha_actual = date.today()
    
        # generamos los ultimos 7 dias #
        ultima_semana = []

        for i in range(0,7):
            dia_correspondiente = fecha_actual - timedelta(days=i)
            ultima_semana.append(dia_correspondiente)

        return ultima_semana
    
    @staticmethod
    def obtener_ultima_semana_formateada() -> list[str]:
        ultima_semana = Fecha.obtener_ultima_semana()
        ultima_semana_formateada = []
        for dia in ultima_semana:
            dia_formateado = dia.strftime("%d de %B de %Y").title()
            ultima_semana_formateada.append(dia_formateado)

        return ultima_semana_formateada









    


