class Examen:
    def __init__(self,id_examen:int ,id_materia: int,nombre:str, fecha: str, hora: str, nota: int):
        self.id_examen = id_examen
        self.id_materia = id_materia
        self.nombre = nombre
        self.fecha = fecha
        self.hora = hora
        self.nota = nota