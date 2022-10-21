'''
    Tipos de datos extras para la codificacion de alfabetos.
'''


# Librerias de terceros.
import numpy


class Notacion_Binaria(object):

    def __init__(
        self,
        bits: str,
        periodo: 'int | numpy.inf',
        inicio_periodo: int,
    ) -> None:
        self.bits = bits
        self.periodo = periodo
        self.inicio_periodo = inicio_periodo

    def __str__(self) -> str:
        '''
            Crea una representacion string de la notacion binaria.
        '''

        msg = '(0.'

        for i in range(len(self.bits)):

            if i < self.inicio_periodo:
                msg  += self.bits[i]

            else:
                msg += self.bits[i] + '\u0305'

        msg += ')2'
        return msg