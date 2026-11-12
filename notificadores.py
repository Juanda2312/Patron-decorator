"""Biblioteca de notificaciones resuelta con el patrón Decorator."""
from abc import ABC, abstractmethod


class Notificador(ABC):
    """Componente: interfaz común de notificadores y decoradores."""

    @abstractmethod
    def enviar(self, mensaje: str) -> None:
        ...


class NotificadorEmail(Notificador):
    """Componente concreto: el comportamiento base (correo electrónico)."""

    def __init__(self, correos: list[str]) -> None:
        self._correos = correos

    def enviar(self, mensaje: str) -> None:
        print(f"[Email a {', '.join(self._correos)}] {mensaje}")


class NotificadorDecorador(Notificador):
    """Decoradora base: guarda el notificador envuelto y le delega todo."""

    def __init__(self, envuelto: Notificador) -> None:
        self._envuelto = envuelto

    def enviar(self, mensaje: str) -> None:
        self._envuelto.enviar(mensaje)


class NotificadorSMS(NotificadorDecorador):
    def __init__(self, envuelto: Notificador, telefono: str) -> None:
        super().__init__(envuelto)
        self._telefono = telefono

    def enviar(self, mensaje: str) -> None:
        super().enviar(mensaje)
        print(f"[SMS a {self._telefono}] {mensaje}")


class NotificadorSlack(NotificadorDecorador):
    def __init__(self, envuelto: Notificador, canal: str) -> None:
        super().__init__(envuelto)
        self._canal = canal

    def enviar(self, mensaje: str) -> None:
        super().enviar(mensaje)
        print(f"[Slack {self._canal}] {mensaje}")


class NotificadorFacebook(NotificadorDecorador):
    def __init__(self, envuelto: Notificador, usuario: str) -> None:
        super().__init__(envuelto)
        self._usuario = usuario

    def enviar(self, mensaje: str) -> None:
        super().enviar(mensaje)
        print(f"[Facebook a {self._usuario}] {mensaje}")
