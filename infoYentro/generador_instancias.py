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
import datetime
import argparse

# Librerias de tercer
import numpy as np

# Librerias propias.
from util.constantes import Tipo_Operacion
from util.funciones import generar_frecuencias, generar_matriz_transiciones
from util.archivos import guardar_instancia


# Genera un nombre default para el archivo salida.
def get_default_file_name() -> str:
    hoy = datetime.datetime.now()

    archivo_salida = 'instancia-{}{}{}{}'.format(
        hoy.day,
        hoy.hour,
        hoy.minute,
        hoy.second
    )

    return archivo_salida


# Formatea los argumentos pasados por consola.
def format_args() -> argparse.Namespace:
    args_parser = argparse.ArgumentParser(
        description='Generador de instancias de información mutua y entropia'
    )

    args_parser.add_argument(
        '--arch_salida',
        default=get_default_file_name(),
        help='Nombre del archivo salida',
        dest='nombre_archivo',
        type=str,
    )

    args_parser.add_argument(
        '--data_long',
        default=None,
        help='Total de datos en la instancia',
        dest='total_datos',
        type=int,
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

    args_parser.add_argument(
        '--seed',
        default=0,
        help='Semilla para generar la instancia',
        dest='seed',
        type=int,
    )

    args_parser.add_argument(
        '--as_csv',
        default=False,
        help='Guarda la instancia como un archivo CSV',
        dest='as_csv',
        type=bool,
    )

    args_parser.add_argument(
        '--as_matriz',
        default=False,
        help='Guarda la instancia como una matriz de transiciones',
        dest='as_matriz',
        type=bool,
    )

    args = args_parser.parse_args()

    return args


# Funcion main.
def main(con_args: argparse.Namespace, *args, **kargs) -> None:
    # Registramos el tiempo de inicio de la creacion de la instancia.
    a = time.perf_counter()

    # Cargamos los parametros pasados por consola.
    nombre_archivo: str = con_args.nombre_archivo
    total_datos: int = con_args.total_datos
    tipo_operacion: int = con_args.tipo_operacion
    seed: int = con_args.seed
    as_csv: bool = con_args.as_csv
    as_matriz: bool = con_args.as_matriz

    # Instanciamos la semilla.
    np.random.seed(seed)

    # Instanciamos el tipo de operacion que sera la instancia.
    if tipo_operacion == 1:
        tipo_operacion = Tipo_Operacion.CUANTIFICABLE

    elif tipo_operacion == 2:
        tipo_operacion = Tipo_Operacion.TRANSMISION_DATOS

    elif tipo_operacion == 3:
        tipo_operacion = Tipo_Operacion.TRANSICION_ESTADOS

    else:
        raise Exception('Tipo de operacion invalido!')

    print(
        '---> Tipo de operación seleccionada: {}'.format(
            tipo_operacion.name
        )
    )

    # Generamos un dataframe con las frecuencias dadas.
    frecuencias = None
    if tipo_operacion is Tipo_Operacion.TRANSICION_ESTADOS and as_matriz:
        frecuencias = generar_matriz_transiciones(
            total_datos,
            total_datos*10
        )

    else:
        frecuencias = generar_frecuencias(total_datos)

    print('---> Frecuencias generadas\n')
    print(frecuencias)

    # Registramos el tiempo de finalizacion de la
    # creacion de la instancia.
    b = time.perf_counter()

    # Imprimimos el tiempo que se tomo para crear la instancia.
    print('\n---> Instancia creada en {0:.2f} segundos'.format(b - a))

    # Serializamos la instancia en un archivo binario.
    guardar_instancia(nombre_archivo, frecuencias, tipo_operacion, as_csv)

    print('---> Generacion de instancia terminada')


if __name__ == "__main__":
    # Limpiamos la consola.
    os.system('clear')

    # Formateamos los parametros pasados por consola.
    con_args = format_args()

    if con_args.total_datos is None or con_args.tipo_operacion is None:
        mensaje = 'Es necesario llenar todos los parametros'
        mensaje += ', usa -h para mostrar la ayuda'

        raise Exception(
            mensaje
        )

    # Ejecutamo la funcion main.
    main(con_args)
