from datetime import date, timedelta
import locale

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

def obtener_ultima_semana() -> list[date]:
    # obtenemos la fecha actual #
    fecha_actual = date.today()
    
    # generamos los ultimos 7 dias #
    ultima_semana = []

    for i in range(0,7):
        dia_correspondiente = fecha_actual - timedelta(days=i)
        ultima_semana.append(dia_correspondiente)

    return ultima_semana

def obtener_ultima_semana_formateada() -> list[str]:
    ultima_semana = obtener_ultima_semana()
    ultima_semana_formateada = []
    for dia in ultima_semana:
        dia_formateado = dia.strftime("%d de %B de %Y").title()
        ultima_semana_formateada.append(dia_formateado)

    return ultima_semana_formateada

        

    

obtener_ultima_semana_formateada()
    