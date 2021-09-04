'''
    Programa para T1 de TIMC.
'''


# !/usr/bin/env python3
# -*- coding: UTF-8 -*-


# Librerias estandar.
import sys
import random

# Librerias de tercer
from progress.bar import Bar
import numpy as np

# Librerias propias.
from util.funciones import informacion_mutua, entropia
from util.constantes import Tipo_Operacion


# Funcion main.
def main(args):
    datos = np.array(
        [0.3, 0.21, 0.17, 0.13, 0.09, 0.07, 0.01, 0.02],
        dtype=float
    )
    tipo_operacion = Tipo_Operacion.TANSMISION_DATOS
    print(entropia(datos, tipo_operacion))


if __name__ == "__main__":
    try:
        main(sys.argv[1:])

    except Exception as error:
        print('Ocurrio un error: {}'.format(error))
