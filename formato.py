"""Decoradores de formato. Se agregan sin tocar notificadores.py."""
from datetime import datetime
from typing import Callable

from notificadores import Notificador, NotificadorDecorador


class MensajeEnMayusculas(NotificadorDecorador):
    """Cambia el mensaje ANTES de pasarlo al objeto envuelto."""

    def enviar(self, mensaje: str) -> None:
        super().enviar(mensaje.upper())


class MensajeConMarcaDeTiempo(NotificadorDecorador):
    """Antepone la hora al mensaje antes de pasarlo al objeto envuelto."""

    def __init__(self, envuelto: Notificador,
                 reloj: Callable[[], str] | None = None) -> None:
        super().__init__(envuelto)
        self._reloj = reloj or (lambda: datetime.now().strftime("%H:%M:%S"))

    def enviar(self, mensaje: str) -> None:
        super().enviar(f"[{self._reloj()}] {mensaje}")
