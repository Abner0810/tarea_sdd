# Tests para habitos/repositorio.py

import os
import tempfile
import unittest
from habitos import repositorio


class TestRepositorio(unittest.TestCase):
    def test_leer_crea_archivo_si_no_existe(self):
        fd, ruta = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        os.unlink(ruta)
        datos = repositorio.leer(ruta)
        self.assertIn('habitos', datos)
        self.assertEqual(datos['habitos'], [])
        os.unlink(ruta)

    def test_guardar_y_leer(self):
        fd, ruta = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        os.unlink(ruta)
        datos = {'habitos': [{'nombre': 'Beber agua', 'marcas': []}]}
        repositorio.guardar(datos, ruta)
        cargado = repositorio.leer(ruta)
        self.assertEqual(cargado['habitos'][0]['nombre'], 'Beber agua')
        os.unlink(ruta)


if __name__ == '__main__':
    unittest.main()
