'''
    Codificación de alfabetos, se utilizan distintos metodos
    para codificar alfabetos.
'''


# !/usr/bin/env python3
# -*- coding: UTF-8 -*-


# Librerias estandar.
import sys
import time
from os import system
from requests import get

# Librerias de terceros.
import numpy

# Librerias propias.
from util.funciones import pre_analisis
from esquema.huffman import Arbol_Hunffman_Modificado, Arbol_Huffman


# Funcion main.
def main(archivo_entrada=None):
    system('clear')

    if archivo_entrada is None:
        try:
            # req = get('https://loripsum.net/api/100/verylong/plaintext')
            req = get('https://loripsum.net/api/10/verylong/plaintext')
            # req = get('https://loripsum.net/api/1/short/plaintext')

            texto = ''
            for r in req:
                texto += r.decode('utf-8')

        except Exception:
            print('---> Request negado\n')
            texto = '''
                Server data formats are used to be the cover medium in
                data hiding, e.g. audio files, video files, image files, text files,
                and so on. Although the data structure of text files is similar
                to image files than the other data format mentioned above,
                most of image data hiding schemes are not suitable for text
                files. The main reason is that most image data hiding
                schemes embed secret information into cover image by
                slightly perturbing the pixel values. Since gray-scale or color
                images can tolerant a small amount modifications of pixel
                values, it will cause no perceptible distortions. On the
                contrary, any changes in the text file might lead to
                meaningless content.
                Few studies have referred to hiding secret messages in
                text files. In [1], the data was embedded by modifying the
                inter-character space, but it resulted in some distortions in
                the shape of words. In [3], a technique was proposed for
                copyright protection that marks the text file by shifting lines
                up or down and words right or left; however, the technique
                might change the typesetting of the text file accordingly.
                In addition to the security problem, bandwidth
                consumption is also an important concern. The size of
                transmitted files can be reduced by either of two categories
                of data compression technology: lossless and lossy
                technologies. The lossy data compression technology is
                widely used in images, but it may be unsuitable for text files
                because any loss of data may lead the content meaningless.
            '''

    else:
        objeto_archivo = open(archivo_entrada, 'r')
        texto = objeto_archivo.read()
        objeto_archivo.close()

    print('---> Texto Cargado')
    print(texto)
    print()

    i = time.time()
    a, f = pre_analisis('hola')
    arb = Arbol_Huffman(a, f)
    arb.generar_tabla_codigos()
    secreto_bin = arb.codificar('hola')
    j = time.time()

    tiempo_secreto = j - i

    print('---> Secreto bin')
    print(secreto_bin)
    print()

    i = time.time()
    print('---> Pre-Análisis realizado')
    alfabeto, frecuencias = pre_analisis(texto)
    j = time.time()
    tiempo_frec_txt = j - i

    print('---> Agregamos Mx y ES y sus frecuencias')
    alfabeto['ES'] = 'ES'
    alfabeto['Mx'] = 'Mx'

    frecuencias['ES'] = 0
    frecuencias['Mx'] = numpy.Inf

    print('---> Alfabeto')
    print(alfabeto)
    print()

    print('---> Frecuencias')
    print(frecuencias)
    print()

    huffman = Arbol_Hunffman_Modificado(
        alfabeto,
        frecuencias
    )

    i = time.time()
    print('---> Generando tabla de codificacion')
    huffman.generar_tabla_codigos()
    print('---> Tabla derecha')
    print(huffman.tabla_codificacion_derecha)
    print()
    print('---> Tabla izquerda')
    print(huffman.tabla_codificacion_izquierda)
    print()
    j = time.time()
    tiempo_generar_tablas = j - i

    i = time.time()
    print('---> Codificando el texto')
    stego = huffman.codificar(texto, secreto_bin)
    print(stego)
    print()
    j = time.time()
    tiempo_codificacion = j - i

    i = time.time()
    print('---> Decodificando el texto codificado')
    texto_decodificado, secreto = huffman.decodificar(stego)
    print(texto_decodificado)
    print()
    j = time.time()
    tiempo_decodificacion = j - i

    print('---> Secreto recuperado')
    print(arb.decodificar(secreto))
    print()

    with open("reporte_texto_largo.txt", 'w+', encoding='utf-8') as objeto_archivo:
        objeto_archivo.write("Texto:\n{}\n".format(texto))
        objeto_archivo.write("Total de caracteres en el texto: {}\n".format(
            len(texto)
        ))
        objeto_archivo.write("Secreto:\n{}\n".format(secreto_bin))
        objeto_archivo.write("Total de bits en el secreto: {}\n".format(
            len(secreto_bin)
        ))
        objeto_archivo.write("Alfabeto:\n{}\n".format(a.to_string()))
        objeto_archivo.write("Frecuencias:\n{}\n".format(f.to_string()))

        objeto_archivo.write("Tabla de codificacion derecha:\n{}\n".format(
            huffman.tabla_codificacion_derecha.to_string()
        ))
        objeto_archivo.write("Tabla de codificacion izquierda:\n{}\n".format(
            huffman.tabla_codificacion_izquierda.to_string()
        ))

        objeto_archivo.write("Tiempo de codificacion del secreto: {0:.2f}s\n".format(
            tiempo_secreto
        ))
        objeto_archivo.write("Tiempo de analisis del texto: {0:.2f}s\n".format(
            tiempo_frec_txt
        ))
        objeto_archivo.write("Tiempo de generacion de tablas: {0:.2f}s\n".format(
            tiempo_generar_tablas
        ))
        objeto_archivo.write("Tiempo de codificacion del texto: {0:.2f}s\n".format(
            tiempo_codificacion
        ))
        objeto_archivo.write("Tiempo de decodificacion del codigo: {0:.2f}s\n".format(
            tiempo_decodificacion
        ))

if __name__ == "__main__":
    main(*sys.argv[1:])
