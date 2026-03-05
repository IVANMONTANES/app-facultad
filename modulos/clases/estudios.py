from modulos.clases.fechas import Fecha

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
        from modulos.db import estudioDb
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
        