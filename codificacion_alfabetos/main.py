'''
    Codificación de alfabetos, se utilizan distintos metodos
    para codificar alfabetos.
'''


# !/usr/bin/env python3
# -*- coding: UTF-8 -*-


# Librerias estandar.
import os
import argparse
from requests import get

# Librerias de terceros.
from simhash import Simhash

# Librerias propias.
from util.funciones import pre_analisis
from util.archivos import cargar_archivo
from esquema.huffman import Huffman_Jerarquico, Huffman_Balanceado
from esquema.estadisticos import Shannon


# Formatea los argumentos pasados por consola.
def format_args() -> argparse.Namespace:
    args_parser = argparse.ArgumentParser(
        description='Programa principal de Información mutua y entropia'
    )

    args_parser.add_argument(
        '--archivo',
        default=None,
        help='Nombre del archivo',
        dest='dir_archivo',
        type=str,
    )

    args_parser.add_argument(
        '--reporte',
        default=None,
        help='Nombre del archivo del reporte de salida',
        dest='dir_reporte',
        type=str
    )

    args = args_parser.parse_args()

    return args


# Funcion main.
def main(con_args: argparse.Namespace, *args, **kargs):
    # Recuperamos los parametros pasados por consola.
    dir_archivo: str = con_args.dir_archivo
    dir_reporte: str = con_args.dir_reporte

    # Cargamos el archivo a comprimir.
    texto = cargar_archivo(dir_archivo)

    print('---> Texto Cargado')
    if len(texto) < 100:
        print(texto)
    else:
        print(texto[:100] + '...')
    print()

    print('---> Pre-Análisis realizado')
    alfabeto, frecuencias = pre_analisis(texto)

    print('---> Alfabeto')
    print(alfabeto)
    print()

    print('---> Frecuencias')
    print(frecuencias)
    print()

    # Instanciamos el esquema a usar.
    huffman = Shannon(
        alfabeto,
        frecuencias,
        len(texto)
    )

    print('---> Generando tabla de codificacion')
    huffman.generar_tabla_codigos()
    print(huffman.tabla_codificacion)
    print()

    print('---> Generando reporte')
    huffman.generar_reporte(dir_reporte)
    print()

    print('---> Codificacion de texto')
    texto_input = 'Μνω'
    texto_codificado = huffman.codificar(texto_input)
    if len(texto_codificado) < 100:
        print(texto_codificado)
    else:
        print(texto_codificado[:100] + '...')
    print()

    print('---> Decodificacion de texto')
    texto_decodificado = huffman.decodificar(texto_codificado)
    if len(texto_decodificado) < 100:
        print(texto_decodificado)
    else:
        print(texto_decodificado[:100] + '...')
    print()

    print('---> Verificando hash del texto')
    hash_original = Simhash(texto_input).value
    hash_decodificado = Simhash(texto_decodificado).value

    if hash_original == hash_decodificado:
        print('---> El texto original coincide con el decodificado')

        # Creamos el archivo del reporte.
        with open(
            dir_reporte + '_texto_codificado.txt',
            'w+',
            encoding='utf-8'
        ) as objeto_archivo:
            objeto_archivo.write(texto_codificado)

    else:
        raise Exception(
            '---> Error: El texto codificado es distinto del original'
            + '\n---> Hash del original {}'.format(hash_original)
            + '\n---> Hash del decodificado {}'.format(hash_decodificado)
        )


if __name__ == "__main__":
    # Limpiamos la consola.
    os.system('clear')

    # Formateamos los parametros pasados por consola.
    con_args = format_args()

    if con_args.dir_archivo is None or con_args.dir_reporte is None:
        raise Exception(
            '---> Es necesario agregar los argumentos'
            + ' ingregar -h para mayor informacion'
        )

    # Ejecutamo la funcion main.
    main(con_args)
