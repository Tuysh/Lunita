from app import Lunita

lunita = Lunita("user_1")

while True:
    pregunta = input("Pregunta: ")
    if pregunta.lower() == "exit":
        break
    print("\nRespuesta: " + lunita.enviar_mensaje(pregunta))
    print("\n")

