# Biblioteca de notificaciones con Decorator

Implementación en Python del patrón Decorator para la actividad de patrones de diseño.

## Requisitos
Python 3.10 o superior. No se usan librerías externas.

## Archivos
- `notificadores.py`: interfaz `Notificador`, `NotificadorEmail`, `NotificadorDecorador`, y los decoradores de SMS, Slack y Facebook.
- `formato.py`: decoradores de formato (`MensajeEnMayusculas`, `MensajeConMarcaDeTiempo`).
- `constructor.py`: constructor fluido para armar la pila de decoradores.
- `cliente.py`: programa de ejemplo que arma la pila según un diccionario de preferencias.
- `test_notificadores.py`: pruebas con `unittest`.

## Ejecución
```
python cliente.py
python -m unittest -v
```

## Notas
Los canales se simulan con `print`. Los decoradores de `formato.py` se agregaron sin modificar `notificadores.py`.
Para que el formato alcance a todos los canales, el decorador de formato debe ser la capa más externa.
