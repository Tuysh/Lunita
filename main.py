from app import Lunita

lunita = Lunita()
pregunta = input("Cuestion: ")
print("Respuesta: " + lunita.send_message(pregunta))
