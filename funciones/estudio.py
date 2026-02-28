from datetime import date



class Estudio:
    def __init__(self,id_estudio:int ,horas_estudio:int, fecha: str):
        self.id_estudio = id_estudio
        self.horas_estudio = horas_estudio
        self.fecha = fecha


def sumar_horas_estudio(estudios: list[Estudio]):
    total_horas = 0
    for estudio in estudios:
        total_horas += estudio.horas_estudio
    return total_horas



