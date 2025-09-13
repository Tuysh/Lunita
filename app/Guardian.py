from .Client import client


class Guardian:
    def _analiceMessage(self, message: str):
        """
        Funcion para mandar mensaje a la API de Open Router
        """
        return client.moderations.create(model="omni-moderation-latest", input=message)

    def getVeredict(self, message: str) -> bool:
        """
        Funcion ananliza y devuelve si un mensaje cumple con las directrices
        """
        if self._analiceMessage(message).results[0].flagged:
            return False

        return True
