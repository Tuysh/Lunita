from app import Lunita

lunita = Lunita()
pregunta = "Te quiero mucho"
print("Pregunta: " + pregunta)
print("Respuesta: " + lunita.send_message(pregunta))
