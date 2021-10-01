"""
    Clase de nodos para el arbol de combinaciones
"""


# Clase nodo contenida en el arbol de combinaciones.
class Nodo(object):
    """
        Clase de nodo para el arbol de combinaciones,
        contiene un id, el contenido del nodo.
    """

    # Constructor de clase.
    def __init__(self, id_nodo, contenido, padre, hijos, costos):
        self.id_nodo = id_nodo
        self.contenido = contenido
        self.padre = padre
        self.hijos = hijos
        self.costos = costos

    def __str__(self):
        mensaje = 'id: {}, id padre: {}, id hijos: {}'
        mensaje += ', contenido: {}, costos: {}'

        return mensaje.format(
            self.id_nodo,
            self.padre,
            self.hijos,
            self.contenido,
            self.costos
        )

    def costo_de(self, id_hijo):
        index = self.hijos.index(id_hijo)
        return self.costos[index]

    def es_hoja(self):
        return False if len(self.hijos) > 0 else True

    def es_raiz(self):
        return True if len(self.padre) is None else False
