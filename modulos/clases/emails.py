from modulos.db import examenDb,materiasDb
from modulos.clases.fechas import Fecha
import smtplib
from datetime import datetime
import locale
from email.message import EmailMessage

locale.setlocale(locale.LC_TIME,"es_AR.UTF-8")

class Email:
    @staticmethod
    def notificar_examenes_proximos() -> None:
        """
        funcion que se encarga de enviar un mail con los examanes de hoy y mañana, y marcarlos como notificados

        parametros:
            no recibe

        comportamiento:
            - obtiene la lista de examenes a notificar 
            - si la lista tiene examenes, contruye el mensaje que se enviara por mail, y se trata de enviarlo.
            - se llama a la funcion marcar_examen_como_notificado, que se encarga de marcar los examenes como notificados

        retorna:
            None: no retorna nada

        """
        

        # obtiene la lista de los examenes que deben ser notificados #
        examenes_a_notificar = examenDb.obtener_examenes_no_notificados()
        
        # verificamos que haya examanes que deban ser notificados #
        if examenes_a_notificar:
        
            # contruimos el mensaje que se enviara por mail #
            mensaje = "-------------------- EXAMENES PROXIMOS --------------------\n"
            for examen in examenes_a_notificar:
                # formato en que viene la fecha #
                formato = "%Y-%m-%d"
                # obtenemos la fecha en el formato adecuado #
                fecha_formateada = Fecha.formatear_fecha(examen.fecha,formato)
                mensaje += "------------------------------\n"
                mensaje += f"MATERIA: {materiasDb.obtener_materia(examen.id_materia).nombre}\n"
                mensaje += f"{examen.nombre.upper()} - {fecha_formateada.upper()} A LAS {examen.hora}\n"

            # creamos el mail #
            msg = EmailMessage()
            msg["Subject"] = "PROXIMOS PARCIALES"
            msg["From"] = "pruebasfilipit@gmail.com"
            msg["To"] = "ivanmontanesfilipit@gmail.com"
            msg.set_content(mensaje)

            # tratamos de enviar el mail #
            try:
                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                    smtp.login("pruebasfilipit@gmail.com","c j l n l a o c e o x q m h s a")
                    smtp.send_message(msg)
            
                # marcamos los examenes como notificados #
                for examen in examenes_a_notificar:
                    examenDb.marcar_examen_como_notificado(examen.id_examen)

            except Exception as e:
                print("ocurrio un error al enviar el mail")

        print("no hay examenes que deban ser notificados")
        