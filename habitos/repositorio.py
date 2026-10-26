# Repositorio para persistencia JSON (unico archivo)

import json
import os

RUTA_POR_DEFECTO = os.path.join(os.path.dirname(__file__), 'datos', 'habitos.json')


def leer(ruta=None):
    if ruta is None:
        ruta = RUTA_POR_DEFECTO
    if not os.path.exists(ruta):
        directorio = os.path.dirname(ruta)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        datos_iniciales = {'habitos': []}
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(datos_iniciales, f, ensure_ascii=False, indent=2)
        return datos_iniciales
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)


def guardar(datos, ruta=None):
    if ruta is None:
        ruta = RUTA_POR_DEFECTO
    directorio = os.path.dirname(ruta)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio)
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
