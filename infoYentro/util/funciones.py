# !/usr/bin/env python3
# -*- coding: UTF-8 -*-


# Librerias de terceros.
import numpy as np
import pandas as pd
from progress.bar import ChargingBar as Barra

# Librerias propias.
from util.constantes import Tipo_Operacion


# Calcula la informaicon mutua de un conjunto
# retorna la sumatoria de esta y el valor por dato.
def Ie(
    frecuencias: 'pd.Series',
    operacion: 'Tipo_Operacion'
) -> 'pd.Series':
    # Se obtiene cual es el operdor del logaritmo a usar.
    if operacion is Tipo_Operacion.CUANTIFICABLE:
        log = np.log10
    elif operacion is Tipo_Operacion.TRANSMISION_DATOS:
        log = np.log2
    elif operacion is Tipo_Operacion.TRANSICION_ESTADOS:
        log = np.log
    else:
        raise Exception('El tipo de operación no es valido')

    informacion_mutua = -log(frecuencias)

    return informacion_mutua


# Calcula la entropia de un conjunto
# retorna la sumatoria de esta y el valor por dato.
def He(
    frecuencias: 'pd.Series',
    informacion_mutua: 'pd.Series',
) -> 'pd.Series':
    entropia = frecuencias * informacion_mutua

    return entropia


# Generador de estados para la matriz de transiciones.
def generador_estados(total_estados: int, estados: 'list[str]') -> None:
    for _ in range(total_estados):
        yield np.random.choice(estados)


# Genera un dataframe con una matriz de transiciones de estados.
def generar_matriz_transiciones(
    total_variables: int,
    N: int = 100
) -> pd.DataFrame:
    # Instanciamos un diccionario que contendra los conteos de las
    # variables.
    estados = {}

    # Instanciamos una barra de progreso.
    barra = Barra('---> Creando Matriz de Estados', max=total_variables)

    # Generamos un index para los estados.
    for i in range(total_variables):
        estados['E{}'.format(i)] = 0.0
        barra.next()
    barra.finish()

    # Creamos la matriz de transiciones de estados, con valores en 0.
    matriz_transicion_estados = pd.DataFrame(
        estados,
        index=list(estados.keys()),
        dtype=np.float64
    )

    # Revizamos la frecuencia del cambio de destados en el patron.
    patrones = generador_estados(N, list(estados.keys()))
    E0 = patrones.__next__()
    for Ei in patrones:
        matriz_transicion_estados[E0][Ei] += 1
        E0 = Ei

    # Caculamos la frecuencia como tal de la matriz de transiciones.
    for id_columna in matriz_transicion_estados:
        columna = matriz_transicion_estados.loc[:, id_columna]
        sumatoria = sum(columna)
        columna /= sumatoria

    return matriz_transicion_estados


# Genera una serie con frecuencias aleatorias.
def generar_frecuencias(total_variables: int) -> pd.Series:
    '''
        Genera un dataframe con frecuencias aleatorias.
    '''

    # Instanciamos un diccionario que contendra los conteos de las
    # variables.
    variables = {}

    # Instanciamos una barra de progreso.
    barra = Barra('---> Creando instancia', max=total_variables)

    # Generamos un conteo aleatior para la variable, entre 1 a 100.
    for i in range(total_variables):
        variables['f{}'.format(i)] = np.random.randint(1, 100)
        barra.next()
    barra.finish()

    # Creamos una serie en pandas que contenga el conteo.
    datos = pd.Series(
        variables,
        dtype=np.int64
    )

    # Calculamos la frecuencia de los datos.
    frecuencia = datos / sum(datos)

    return frecuencia