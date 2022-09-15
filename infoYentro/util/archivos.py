'''
'''


# !/usr/bin/env python3
# -*- coding: UTF-8 -*-


# Librerias estandar.
import sys
import pickle
import pathlib

# Librerias de terceros.
import pandas as pd
import numpy as np

# Librerias propias
from util.constantes import Tipo_Operacion


# Cargamos la instancia de un archivo csv.
def cargar_instancia_csv(
    directorio: 'pathlib.Path'
) -> 'pd.Series | pd.DataFrame':
    # Verificamos si el archivo no existe, si no existe
    # muestra una excepcion.
    if not directorio.is_file():
        raise Exception(
            "el archivo {} no existe!".format(directorio)
        )
    
    print('---> Cargando instancia csv')

    # Cargamos la instancia del .csv por medio de numpy.
    datos = np.genfromtxt(directorio, delimiter=',')

    # Si la instancia es una matriz, creamos un dataframe.
    if len(datos.shape) > 1:
        # Creamos el dataframe que contenga los datos.
        variables = {}
        i = 0
        for x in range(datos.shape[1]):
            variables['f{}'.format(i)] = 0
            i += 1

        instancia = pd.DataFrame(variables, index=list(variables.keys()))

        # Guardamos los datos en el dataframe.
        instancia += datos

    # Si es un array, creamos una serie.
    else:
        variables = {}
        i = 0
        for dato in datos:
            variables['f{}'.format(i)] = dato
            i += 1
            
        instancia = pd.Series(variables)

    return instancia



# Cargamos la instancia de un archivo serializado.
def cargar_instancia(directorio: 'pathlib.Path') -> dict:
    # Verificamos si el archivo no existe, si no existe
    # muestra una excepcion.
    if not directorio.is_file():
        raise Exception(
            "el archivo {} no existe!".format(directorio)
        )
    
    print('---> Cargando instancia serializada')

    # Se abre el fichero si se carga desde un fim.
    fichero = open(directorio, "rb")

    # Se carga el archivo serializado.
    informacion = pickle.load(fichero)

    return informacion


# Guardamos la instancia como un archivo serializado.
def guardar_instancia(
    nombre_archivo: str,
    instancia: pd.DataFrame,
    tipo_instancia: Tipo_Operacion,
    as_csv: bool,
) -> None:
    nombre_archivo += '.csv' if as_csv else '.fime'
    directorio = pathlib.Path(nombre_archivo)

    # Verificamos que el archivo no exista.
    if directorio.is_file():
        raise Exception(
            "el archivo con el nombre {} ya existe!".format(nombre_archivo)
        )

    print('---> Serializando instancia')

    # Creamos el archivo binario.
    with open(nombre_archivo, 'wb+') as archivo:
        if as_csv:
            instancia.to_csv(nombre_archivo)

        else:
            pickle.dump(
                {
                    'instancia': instancia,
                    'tipo_operacion': tipo_instancia,
                },
                archivo,
                protocol=pickle.HIGHEST_PROTOCOL
            )

    print('---> Instancia guardada')