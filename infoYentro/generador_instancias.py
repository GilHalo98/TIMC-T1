'''
    Generador de instancias.

    Parametros:
        - Tipo de proceso.
        - Dimencion de array / matriz.
        - Nombre de archivo de salida, opcional.
'''


# !/usr/bin/env python3
# -*- coding: UTF-8 -*-


# Librerias estandar.
import sys
import pickle
import datetime

# Librerias de tercer
import numpy as np

# Librerias propias.
from util.constantes import Tipo_Operacion

# Funcion main.
def main(tipo_operacion, dimenciones, archivo_salida=''):
    # Asignamos una semilla.
    np.random.seed(0)

    # Si no existe un nombre para el archivo de salida, se asigna uno.
    if archivo_salida == '':
        hoy = datetime.datetime.now()
        archivo_salida = 'instancia-{}{}{}{}'.format(
            hoy.day,
            hoy.hour,
            hoy.minute,
            hoy.second
        )

    archivo_salida += '.fime'

    # Se verifica el tipo de operacion.
    if tipo_operacion == 'cuantificable':
         tipo_operacion = Tipo_Operacion.CUANTIFICABLE
    elif tipo_operacion == 'datos':
         tipo_operacion = Tipo_Operacion.TRANSMISION_DATOS
    elif tipo_operacion == 'estados':
         tipo_operacion = Tipo_Operacion.TRANSICION_ESTADOS
    else:
        raise Exception(
            'El tipo de operación {} no es valido'.format(tipo_operacion)
        )

    # Asignamos las dimenciones de los datos.
    dimenciones = [
        int(dimencion) for dimencion in dimenciones.split('x')
    ]

    dimenciones.reverse()

    datos = np.random.rand(*dimenciones)

    # Creando un fichero en escritura binaria
    fichero = open(archivo_salida, "wb")

    # Se serealizan los datos con pickle.
    pickle.dump(
        {
            'tipo operacion': tipo_operacion,
            'datos': datos,
        },
        fichero
    )

    # Cerrando el objeto archivo
    fichero.close()


if __name__ == "__main__":
    main(*sys.argv[1:])
