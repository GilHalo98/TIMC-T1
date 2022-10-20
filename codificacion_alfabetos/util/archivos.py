'''
    Codificación de alfabetos, se utilizan distintos metodos
    para codificar alfabetos.
'''


# !/usr/bin/env python3
# -*- coding: UTF-8 -*-


# Librerias estandar.
import pathlib

# Librerias de terceros
import PyPDF2


def cargar_archivo(dir_archivo: str) -> str:
    '''
        Carga un archivo de texto .txt o .pdf
    '''

    # Texto del archivo cargado.
    texto = ''

    # Directorio del archivo.
    directorio = pathlib.Path(dir_archivo)

    # Formato del archivo
    formato = directorio.suffix.lower()

    # Si el archivo es de formato PDF.
    if formato == '.pdf':
        # Instanciamos un objeto archivo PDF.
        objeto_archivo = PyPDF2.PdfFileReader(directorio)

        # Iteramos por cada pagina.
        for pagina in range(objeto_archivo.numPages):
            # Recuperamos un objeto pagina.
            objeto_pagina = objeto_archivo.getPage(pagina)

            # La concatenamos al texto.
            texto += objeto_pagina.extractText()

    # Si el archivo es de formato TXT.
    if formato == '.txt':
        # Se instancia el objeto archivo.
        objeto_archivo = open(directorio, 'r', encoding='utf-8')

        # Por cada linea del archivo.
        for linea in objeto_archivo:

            # La linea se contactena con el texto.
            texto += linea

    return texto