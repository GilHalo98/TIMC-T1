"""
    Clase nodo para un arbol binario.
"""


# Clase nodo contenida en el arbol de combinaciones.
class Nodo(object):
    """
        Clase nodo para un arbol binario, contiene el padre, el hijo a
        la izquierda y la derecha, así como sus respectivos pesos.

        Contiene el contenido del nodo y un id del mismo. Funciones para
        saber si es hoja o raiz.
    """

    # Constructor de clase.
    def __init__(
        self,
        id_nodo,
        contenido,
        padre=None,
        hijo_izquierda=None,
        hijo_derecha=None,
        costo_izquierda=0,
        costo_derecha=1,
    ):
        self.id_nodo = id_nodo
        self.contenido = contenido
        self.padre = padre
        self.hijo_izquierda = hijo_izquierda
        self.hijo_derecha = hijo_derecha
        self.costo_izquierda = costo_izquierda
        self.costo_derecha = costo_derecha

    def __str__(self):
        mensaje = 'id: {}, padre: {}, contenido: {}'
        mensaje += ', hijo izquierda: {} hijo derecha: {}'

        return mensaje.format(
            self.id_nodo,
            self.padre,
            self.contenido,
            self.hijo_izquierda,
            self.hijo_derecha,
        )

    def es_hoja(self):
        if self.hijo_izquierda is None and self.hijo_derecha is None:
            return True
        return False

    def es_raiz(self):
        return True if self.padre is None else False
