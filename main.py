import asyncio
from app import Lunita

lunita = Lunita("user_1")

async def main():
    while True:
        pregunta = input("Pregunta: ")
        try:
            if pregunta.lower() == "exit":
                break

            respuesta = await lunita.predecir(pregunta)
            print("\nRespuesta: " + respuesta)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
