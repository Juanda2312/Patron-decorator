"""Constructor fluido para armar la pila sin una cadena de if."""
from formato import MensajeConMarcaDeTiempo, MensajeEnMayusculas
from notificadores import (Notificador, NotificadorEmail, NotificadorFacebook,
                           NotificadorSlack, NotificadorSMS)


class ConstructorDeNotificador:
    """Cada método agrega una capa. El orden de las llamadas es el orden
    de la pila, de adentro hacia afuera."""

    def __init__(self, correos: list[str]) -> None:
        self._notificador: Notificador = NotificadorEmail(correos)

    def con_sms(self, telefono: str) -> "ConstructorDeNotificador":
        self._notificador = NotificadorSMS(self._notificador, telefono)
        return self

    def con_slack(self, canal: str) -> "ConstructorDeNotificador":
        self._notificador = NotificadorSlack(self._notificador, canal)
        return self

    def con_facebook(self, usuario: str) -> "ConstructorDeNotificador":
        self._notificador = NotificadorFacebook(self._notificador, usuario)
        return self

    def con_marca_de_tiempo(self) -> "ConstructorDeNotificador":
        self._notificador = MensajeConMarcaDeTiempo(self._notificador)
        return self

    def en_mayusculas(self) -> "ConstructorDeNotificador":
        self._notificador = MensajeEnMayusculas(self._notificador)
        return self

    def construir(self) -> Notificador:
        return self._notificador
