# !/usr/bin/env python3
# -*- coding: UTF-8 -*-


# Librerias de terceros.
import numpy as np

# Librerias propias.
from util.constantes import Tipo_Operacion


# Calcula la informaicon mutua de un conjunto
# retorna la sumatoria de esta y el valor por dato.
def informacion_mutua(datos, operacion, es_matriz=False):
    if es_matriz:
        datos = np.array(datos).flatten()

    # Excluye los ceros del array.
    datos = datos[datos != 0]
    datos = datos[datos != -1]

    # Se obtiene cual es el operdor del logaritmo a usar.
    if operacion is Tipo_Operacion.CUANTIFICABLE:
        log = np.log10
    elif operacion is Tipo_Operacion.TRANSMISION_DATOS:
        log = np.log2
    elif operacion is Tipo_Operacion.TRANSICION_ESTADOS:
        log = np.log
    else:
        raise Exception('El tipo de operación no es valido')

    print('---| Procesando información mutua... ')
    ie = -log(datos)
    print('---> Terminado ')

    return np.sum(ie), ie


# Calcula la entropia de un conjunto
# retorna la sumatoria de esta y el valor por dato.
def entropia(datos, operacion, es_matriz=False):
    if es_matriz:
        datos = np.array(datos).flatten()

    # Excluye los ceros del array.
    datos = datos[datos != 0]
    datos = datos[datos != -1]

    sum_ie, ie = informacion_mutua(datos, operacion)

    print('---| Procesando entropia... ')
    he = datos * ie
    print('---> Terminado ')

    return np.sum(he), he, sum_ie, ie
