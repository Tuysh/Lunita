from app import Lunita

lunita = Lunita("user_1")
pregunta = input("Pregunta: ")
print("Respuesta: " + lunita.send_message(pregunta).output)
