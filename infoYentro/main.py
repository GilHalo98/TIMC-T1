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
import os
import time
import pickle
import pathlib
import argparse

# Librerias de tercer
import numpy as np
import pandas as pd

# Librerias propias.
from util.tui import data_input
from util.funciones import Ie, He
from util.constantes import Tipo_Operacion
from util.archivos import cargar_instancia, cargar_instancia_csv


# Formatea los argumentos pasados por consola.
def format_args() -> argparse.Namespace:
    args_parser = argparse.ArgumentParser(
        description='Programa principal de Información mutua y entropia'
    )

    args_parser.add_argument(
        '--instancia',
        default=None,
        help='Nombre de la instancia',
        dest='instancia',
        type=str,
    )

    args_parser.add_argument(
        '--tipo_operacion',
        default=None,
        help='''
            Tipo de operacion de la instancia
                1: cuantificable
                2: transmicion de datos
                3: tansicion de estados
        ''',
        dest='tipo_operacion',
        type=int,
    )

    args = args_parser.parse_args()

    return args


# Funcion main.
def main(con_args: argparse.Namespace, *args, **kargs) -> None:
    # Cargamos los parametros pasados por consola.
    instancia: str = con_args.instancia
    tipo_operacion: int = con_args.tipo_operacion

    # Instanciamos las variables a usar en el calculo de
    # la entropia y la informacion mutua.
    frecuencias = None

    #  Verificamos como se ingresaran los datos.
    if instancia is None:
        # Si el directorio del archivo instancia no fue pasado por
        # consola, entonces los datos seran ingresados manualmente.
        frecuencias, tipo_operacion = data_input()

    else:
        # Instanciamos el directorio de la instancia.
        directorio = pathlib.Path(instancia)

        if directorio.suffix == '.csv':
            # Si es un arhcivo .csv, entonces se cargan los datos desde
            # el arhivo .csv.

            # Instanciamos el tipo de operacion que sera la instancia.
            if tipo_operacion is None:
                # Tiene que existir un tipo de operacion pasado por
                # parametros.
                raise Exception(
                    '---> Es necesario seleccionar un tipo de operacion!'
                    + ' ingresa -h para mas información.'
                )

            elif tipo_operacion == 1:
                tipo_operacion = Tipo_Operacion.CUANTIFICABLE

            elif tipo_operacion == 2:
                tipo_operacion = Tipo_Operacion.TRANSMISION_DATOS

            elif tipo_operacion == 3:
                tipo_operacion = Tipo_Operacion.TRANSICION_ESTADOS

            else:
                raise Exception('Tipo de operacion invalido!')

            frecuencias = cargar_instancia_csv(directorio)

        elif directorio.suffix == '.fime':
            # Si es un arhcivo .fime, entonces se cargan los datos desde
            # el arhivo .fime.
            datos = cargar_instancia(directorio)

            frecuencias = datos['instancia']
            tipo_operacion = datos['tipo_operacion']

        else:
            raise Exception(
                '---> Tipo de archivo no soportado'
                + ', unicamente se soportan .csv y .fime'
            )

    unidades = ''
    if tipo_operacion is Tipo_Operacion.CUANTIFICABLE:
        unidades = 'hartleys / simbolo'

    elif tipo_operacion is Tipo_Operacion.TRANSMISION_DATOS:
        unidades = 'bits / simbolo'

    elif tipo_operacion is Tipo_Operacion.TRANSICION_ESTADOS:
        unidades = 'nats / simbolo'

    print('---> Instancia cargada')
    print(frecuencias)
    print('---> Tipo de operacion: {}'.format(tipo_operacion))

    es_matriz = True if len(frecuencias.shape) > 1 else False

    if es_matriz:
        print('---> Instancia es matriz, aplanando matriz')

        # Aplanamos la matriz.
        aux_frecuencias = frecuencias.values.flatten()

        # Aquellos valores con frecuencias 0 se omiten.
        aux_frecuencias = aux_frecuencias[aux_frecuencias != 0]

        # Aquellos valores con frecuencias 0 se omiten.
        aux_frecuencias = aux_frecuencias[aux_frecuencias != -1]

        # Asignamos nuevos ids
        valores = {}
        i = 0
        for fi in aux_frecuencias:
            valores['f{}'.format(i)] = fi
            i += 1

        # Guardamos los datos en una Serie.
        frecuencias = pd.Series(valores)
        print('---> Matriz aplanada')
        print(frecuencias)

    informacion_mutua = Ie(frecuencias, tipo_operacion)
    print('---> Información mutua calculada {}'.format(unidades))

    entropia = He(frecuencias, informacion_mutua)
    print('---> Entropia calculada {}'.format(unidades))

    print('---> Informe creado')
    informe = pd.DataFrame(
        {
            'Pe': frecuencias.values,
            'Ie': informacion_mutua.values,
            'He': entropia.values
        },
        index=informacion_mutua.index
    )

    sum_Ie = sum(informacion_mutua)
    sum_He = sum(entropia)

    print(informe)
    
    msj = '---> Información mutua: {0:.2f} '.format(sum(informacion_mutua))
    msj += unidades
    print(msj)

    msj = '---> Entropia: {0:.2f} '.format(sum(entropia))
    msj += unidades
    print(msj)

if __name__ == "__main__":
    # Limpiamos la consola.
    os.system('clear')

    # Formateamos los parametros pasados por consola.
    con_args = format_args()

    # Ejecutamo la funcion main.
    main(con_args)