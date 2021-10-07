"""
    Clase para arbol de combinaciones, supongo que puede ser mucho mas
    eficiente que hacer las permutaciones, pero no estoy muy seguro.
"""


# Librerias de terceros.
from graphviz import Digraph

# Dependencias.
from grafo.nodo import Nodo


class Arbol_Combinaciones(object):
    """
        Clase de arbol de combinaciones.
    """

    # Constructor de clase.
    def __init__(self):
        # Almacena la id de la raiz, por default es 0
        self.id_raiz = 0

        # La topologia del arbol es descrita por un diccionario.
        # Los diccionarios estan compuestos por id: Nodo
        self.topologia = {
            0: Nodo(0, '', None, [], []),
        }

        # Al generar una nueva combinacion, los nodos tiene que ser
        # identificados con un id.
        self.__id = 1

        # Total de combinaciones en el arbol.
        self.total_combinaciones = 0

        # Total de nodos en el arbol.
        self.total_nodos = 1

    def __str__(self):
        recorrido = self.recorrido_preorden()

        _, nodo = next(recorrido)

        arbol = ['{}\n'.format(nodo.id_nodo)]

        nivel_anterior = 0
        nodo_anterior = None
        for nivel, nodo in recorrido:
            representacion = ''

            for _ in range(nivel - 1):
                representacion += '║  '

            if nivel == nivel_anterior:
                if not nodo.es_hoja():
                    representacion += '╠═'
                else:
                    representacion += '╠═'

            else:
                if nivel > nivel_anterior:
                    if nodo.es_hoja():
                        representacion += '╠═'
                    else:
                        representacion += '╠═'
                else:
                    representacion += '╠═'

                    salto = ''
                    for _ in range(nivel_anterior - 1):
                        salto += '║  '
                    arbol[-1] = '{}╚═ {}\n'.format(
                        salto,
                        nodo_anterior.contenido
                    )

            representacion += ' {}\n'.format(nodo.contenido)

            arbol.append(representacion)
            nivel_anterior = nivel
            nodo_anterior = nodo

        mensaje = ''.join(arbol)
        mensaje += '\nTotal de nodos: {}'.format(self.total_nodos)
        mensaje += '\nTotal de combionaciones encontradas: {}'.format(
            self.total_combinaciones
        )
        return mensaje

    def __reset_topologia(self):
        # Al generar un nuevo arbol de combinaciones, resetea la
        # topologia a su estado inicial.
        self.id_raiz = 0

        self.topologia = {
            0: Nodo(0, '', None, [], []),
        }

        self.__id = 1
        self.total_combinaciones = 0
        self.total_nodos = 1

    def __validar_datos(self, caracteres, longitud_canal):
        # Obtenemos los caracteres que puedan ser enviados por el canal.
        caracteres_validos = []
        for caracter in caracteres:
            # Si la longitud del caracter es menor o igual a la longitud
            # del canal, el caracter es seleccionado
            if len(caracter) <= longitud_canal:
                caracteres_validos.append(caracter)

        return caracteres_validos

    def __expandir_nodo(self, id_nodo_actual, caracteres, longitud, costo):
        # Id's de nodos expandidos.
        expancion = []

        # Por cada caracter en los caracteres validos.
        for caracter in caracteres:
            # El costo total es la longitud acutal del mensaje.
            costo_total = costo + len(caracter)

            # Checamos si el costo total es menor o igual que la longitud.
            if costo_total <= longitud:
                # Se instancia un nuevo nodo.
                self.topologia[self.__id] = Nodo(
                    self.__id,
                    caracter,
                    id_nodo_actual,
                    [],
                    []
                )

                # Se enlaza el nodo padre con los hijos.
                self.topologia[id_nodo_actual].hijos.append(self.__id)

                # Se actualizan el peso de las aristas.
                self.topologia[id_nodo_actual].costos.append(costo_total)

                # Agregamos los nodos a la expancion.
                expancion.append(self.__id)

                # Aumentamos el id.
                self.__id += 1

                # Aumentamos la cantidad de nodos.
                self.total_nodos += 1

        # Retorna los nodos expandidos.
        return expancion

    def __get_costo_acumulado(self, id_nodo_actual):
        # Si el nodo actual es la raiz, entonces retorna un costo acumulado
        # de 0, en otro caso, retorna el costo acumulado.
        costo_acumulado = 0
        if id_nodo_actual != self.id_raiz:
            id_padre = self.topologia[id_nodo_actual].padre
            return self.topologia[id_padre].costo_de(id_nodo_actual)

        return costo_acumulado

    def generar_combinaciones(self, caracteres, longitud_canal):
        # Genera las combinaciones con los parametros dados.
        self.__reset_topologia()  # Reseteamos la topologia.

        # Obtenemos los caracteres que puedan ser enviados por el canal.
        caracteres = self.__validar_datos(caracteres, longitud_canal)

        # Si no hay caracteres validos, retorna un error.
        if len(caracteres) <= 0:
            return False

        # Se instancia una frontera, en la cual, mantiene el primer
        # nodo a expandir, que en este caso es la raiz.
        frontera = [self.id_raiz]

        # Ahora empezamos a agreagar los nodos al arbol.
        while True:
            # Se obtiene el id del nodo siguiente en la frontera.
            id_nodo_actual = frontera.pop()

            # Tambien instanciamos una variable que mantenga el costo
            # acumulado de la rama en la que nos encontramos.
            costo_acumulado = self.__get_costo_acumulado(id_nodo_actual)

            # Expandimos el nodo actual.
            expancion = self.__expandir_nodo(
                id_nodo_actual,
                caracteres,
                longitud_canal,
                costo_acumulado,
            )

            # Si la expacion tiene mas de un nodo, se agrega a la frontera
            # sino podemos asumir que encontro una hoja.
            if len(expancion) > 0:
                frontera += expancion
            else:
                # Si no hay nodos en la expacion, eso quiere decir que
                # encontro una hoja.
                self.total_combinaciones += 1

            # Si ya no hay nodos en la frontera, termina el algoritmo.
            if len(frontera) <= 0:
                break

        # Retorna un true para indicar que las combinaciones se hicieron
        # satisfactoriamente.
        return True

    def combinaciones(self):
        # Se mantiene una frontera de exploracion.
        visitados = []

        # Almacena la ruta en la que se encuentra
        ruta = []

        # El id en el que se encuentra actualmente, empieza por la raiz.
        id_nodo_actual = self.id_raiz

        # Mientras que la cantidad de nodos visitados sea menor que
        # la cantidad de nodos en el arbol.
        while len(visitados) < self.total_nodos:
            # Si el nodo visitado no esta marcado, se marca como visitado.
            if id_nodo_actual not in visitados:
                visitados.append(id_nodo_actual)

            # Si el nodo es una hoja se guarda la ruta y se regresa una
            # posicion en el arbol.
            if self.topologia[id_nodo_actual].es_hoja():
                combinacion = [
                    self.topologia[id].contenido for id in ruta.copy()
                ]
                combinacion += [self.topologia[id_nodo_actual].contenido]
                yield ''.join(combinacion)

                id_nodo_actual = ruta.pop()
            else:
                # Por cada hijo en el nodo acutal.
                id_no_visitado = id_nodo_actual
                for id_hijo in self.topologia[id_nodo_actual].hijos:
                    if id_hijo not in visitados:
                        id_no_visitado = id_hijo

                # Si todos los hijos del nodo actual ya fueron visitados.
                if id_nodo_actual == id_no_visitado:
                    # Regresa una posicion en la ruta.
                    id_nodo_actual = ruta.pop()
                else:
                    # Si no es asi, el nodo acutal se marca como ruta.
                    ruta.append(id_nodo_actual)

                    # Se mueve al nodo hijo seleccionado.
                    id_nodo_actual = id_no_visitado

    def nodos_por_nivel(self):
        # Retorna una lista que contiene todos los nodos por nivel visitado.
        nivel = 0  # Nivel en el que se encuentra.
        visitados = 0  # La cantidad de nodos visitados.
        nodos = [self.id_raiz]  # Los id de los nodos en el nivel actual.

        # Mientras que los nodos visitados sean menor que la cantidad total
        # de nodos en el arbol.
        while visitados < self.total_nodos:
            yield nivel, [
                self.topologia[nodo] for nodo in nodos
            ]  # Retorna los nodos por nivel.

            # La expancion son los nodos encontrados por nivel.
            expancion = []

            # Mientras que haya nodos que falten visitar.
            while len(nodos) > 0:
                # Remueve el ultimo id agregado, esto es una cola.
                id_nodo = nodos.pop(0)

                # Aumenta en uno la cantidad de nodos visitados.
                visitados += 1

                # Se agregan los hijos de dicho nodo a la expancion.
                expancion += self.topologia[id_nodo].hijos

            # La expancion se agrega a la cola.
            nodos += expancion

            # Vajamos un nivel en el arbol.
            nivel += 1

    def recorrido_preorden(self):
        # Nodos marcados como visitados.
        visitados = []

        # Id del nodo en el que se encuentra actualmente.
        id_nodo = self.id_raiz

        # El nivel del arbol en el que se encuentra el recorrido.
        nivel = 0

        # Mientras que la cantidad de nodos visitados sea menor a la del
        # total de nodos en el arbol.
        while len(visitados) < self.total_nodos:
            # Si el nodo no esta marcado como visitado.
            if id_nodo not in visitados:
                # Marcamos el nodo como visitado.
                visitados.append(id_nodo)

                # Y retorna el nodo en el que nos encontramos.
                yield nivel, self.topologia[id_nodo]

            # Verificamos si el nodo en el que nos encontramos es hoja.
            if self.topologia[id_nodo].es_hoja():
                # Si es asi, retornamos un nodo.
                id_nodo = self.topologia[id_nodo].padre
                nivel -= 1
            else:
                # Si no es asi, se mueve a un hijo no visitado.
                nuevo_nodo = False
                for id_hijo in self.topologia[id_nodo].hijos:
                    if id_hijo not in visitados:
                        id_nodo = id_hijo
                        nuevo_nodo = True
                        nivel += 1
                        break

                # Si todos los nodos ya fueron visitados, se regresa un nodo.
                if not nuevo_nodo:
                    id_nodo = self.topologia[id_nodo].padre
                    nivel -= 1

    def graficar(self, archivo):
        grafico = Digraph(comment='Test', format='svg')

        for nodo_padre in list(self.topologia.values()):
            grafico.node(
                str(nodo_padre.id_nodo),
                nodo_padre.contenido
            )

            for id_hijo, costo in zip(
                self.topologia[nodo_padre.id_nodo].hijos,
                self.topologia[nodo_padre.id_nodo].costos
            ):
                grafico.edge(
                    str(nodo_padre.id_nodo),
                    str(id_hijo),
                    str(costo),
                )

        grafico.render(filename=archivo)
