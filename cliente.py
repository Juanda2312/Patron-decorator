"""Cliente: arma la pila de decoradores según las preferencias del usuario."""
from formato import MensajeConMarcaDeTiempo, MensajeEnMayusculas
from notificadores import (Notificador, NotificadorEmail, NotificadorFacebook,
                           NotificadorSlack, NotificadorSMS)


def construir_notificador(preferencias: dict) -> Notificador:
    notificador: Notificador = NotificadorEmail(preferencias["correos"])

    # Canales: cada preferencia activa agrega una capa.
    if preferencias.get("sms"):
        notificador = NotificadorSMS(notificador, preferencias["sms"])
    if preferencias.get("slack"):
        notificador = NotificadorSlack(notificador, preferencias["slack"])
    if preferencias.get("facebook"):
        notificador = NotificadorFacebook(notificador, preferencias["facebook"])

    # Formato: va al final para quedar en la capa externa y alcanzar a todos.
    if preferencias.get("marca_de_tiempo"):
        notificador = MensajeConMarcaDeTiempo(notificador)
    if preferencias.get("mayusculas"):
        notificador = MensajeEnMayusculas(notificador)
    return notificador


if __name__ == "__main__":
    usuario_ana = {
        "correos": ["ana@ejemplo.com", "luis@ejemplo.com"],
        "sms": "3001234567",
        "slack": "#alertas",
        "facebook": "ana.perez",
        "marca_de_tiempo": True,
        "mayusculas": True,
    }
    usuario_luis = {"correos": ["luis@ejemplo.com"], "slack": "#soporte"}

    for nombre, prefs in (("Ana", usuario_ana), ("Luis", usuario_luis)):
        print(f"--- Alerta para {nombre} ---")
        construir_notificador(prefs).enviar("Incendio en la casa")
