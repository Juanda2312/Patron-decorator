import io
import unittest
from contextlib import redirect_stdout

from constructor import ConstructorDeNotificador
from formato import MensajeConMarcaDeTiempo, MensajeEnMayusculas
from notificadores import (Notificador, NotificadorEmail, NotificadorFacebook,
                           NotificadorSlack, NotificadorSMS)

CORREOS = ["ana@ejemplo.com"]


def capturar(notificador: Notificador, mensaje: str) -> list[str]:
    """Ejecuta enviar() y devuelve las líneas impresas."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        notificador.enviar(mensaje)
    return buffer.getvalue().splitlines()


class PruebasNotificadores(unittest.TestCase):
    def test_1_sin_decoradores(self):
        lineas = capturar(NotificadorEmail(CORREOS), "alerta")
        self.assertEqual(lineas, ["[Email a ana@ejemplo.com] alerta"])

    def test_2_pila_con_dos_decoradores(self):
        pila = NotificadorSlack(NotificadorSMS(NotificadorEmail(CORREOS), "300"), "#a")
        lineas = capturar(pila, "alerta")
        self.assertEqual(len(lineas), 3)
        self.assertTrue(lineas[0].startswith("[Email"))
        self.assertTrue(lineas[1].startswith("[SMS"))
        self.assertTrue(lineas[2].startswith("[Slack"))

    def test_3_pila_con_tres_decoradores_y_orden(self):
        pila = NotificadorFacebook(
            NotificadorSlack(
                NotificadorSMS(NotificadorEmail(CORREOS), "300"), "#a"), "ana")
        lineas = capturar(pila, "alerta")
        canales = [linea.split(" ")[0] for linea in lineas]
        # El decorador más interno responde primero.
        self.assertEqual(canales, ["[Email", "[SMS", "[Slack", "[Facebook"])

    def test_4_formato_altera_el_mensaje_de_los_demas_canales(self):
        pila = MensajeEnMayusculas(
            NotificadorSMS(NotificadorEmail(CORREOS), "300"))
        lineas = capturar(pila, "alerta")
        self.assertEqual(len(lineas), 2)
        for linea in lineas:
            self.assertTrue(linea.endswith("ALERTA"))

    def test_5_el_orden_de_los_decoradores_cambia_el_resultado(self):
        afuera = MensajeEnMayusculas(
            NotificadorSMS(NotificadorEmail(CORREOS), "300"))
        adentro = NotificadorSMS(
            MensajeEnMayusculas(NotificadorEmail(CORREOS)), "300")
        self.assertEqual(capturar(afuera, "alerta")[1], "[SMS a 300] ALERTA")
        self.assertEqual(capturar(adentro, "alerta")[1], "[SMS a 300] alerta")

    def test_6_marca_de_tiempo_con_reloj_fijo(self):
        pila = MensajeConMarcaDeTiempo(NotificadorEmail(CORREOS), lambda: "12:00:00")
        self.assertEqual(capturar(pila, "alerta"),
                         ["[Email a ana@ejemplo.com] [12:00:00] alerta"])

    def test_7_constructor_equivale_a_la_pila_manual(self):
        manual = MensajeEnMayusculas(
            NotificadorSMS(NotificadorEmail(CORREOS), "300"))
        con_constructor = (ConstructorDeNotificador(CORREOS)
                           .con_sms("300").en_mayusculas().construir())
        self.assertEqual(capturar(manual, "alerta"),
                         capturar(con_constructor, "alerta"))
        self.assertIsInstance(con_constructor, Notificador)


if __name__ == "__main__":
    unittest.main()
