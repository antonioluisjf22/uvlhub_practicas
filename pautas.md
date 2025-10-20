# PAUTAS Y COMANDOS POR CONSOLA M1:

## Pruebas de carga con locust

desde la carpeta raíz del proyecto: locust -f app/modules/notepad/tests/locustfile.py

## ejecución testing rosemary
rosemary test

## ejecución testing pytest
pytest -v

## ejecución archivo específico con pytest
pytest app/modules/notepad/tests/test_unit.py -v
