'''
    Libro El Quijote o el de anna frank
    mitad del libro boyer_moore y la otra mitad KMP
    Patrones de busqueda, "con" y "sin"

    Cantida de coincidencias y posicion de las coincidencias
'''

# Algoritmo Boyer-Moore.
def boyer_moore(t, p):
    '''
        Programarlo con un log de las acciones que el algoritmo realiza.
    '''    
    n = len(t)
    m = len(p)

    i = m - 1
    j = m - 1

    while True:
        # Compara el caracter en P[j] con el de T[i]
        if p[j] == t[i]:
            if j == 0:
                # Se comprueba la comparacion del ultimo caracter del
                # patron, el patron se encuentra en el texto.
                yield i

                i += (m * 2) - 1
                j = m - 1
            else:
                # Mueve la comparacion al siguiente caracter.
                i -= 1
                j -= 1
        else:
            # log += 'Caracteres distintos'
            # La comparacion fallo, se salta m caracteres a la derecha
            # en T.
            ocurrencia_izquierda = last(t[i], p, m)
            i += m - min(j, 1 + ocurrencia_izquierda)

            # Se reinicia la comparacion desde P[m - 1]
            j = m - 1

        if i > n - 1:
            break


# Retorna el primer index encontrado del elemento x, desde
# la derecha hacia la izquierda en el patron.
def last(c, p, m):
    i = m - 1
    while i >= 0:
        if p[i] == c:
            break
        i -= 1
    return i


# Retorna el minimo entre dos datos.
def min(a, b):
    return a if a < b else b


# Algoritmo de Knuth-Morres-Pratt.
def kmp(t, p):
    n = len(t)  # Longitud del texto.
    m = len(p)  # Longitud del patron.

    j = 0  # Index del patron.
    i = 0  # Index del texto.

    # Precomputa el arreglo de lps.
    lps = funcion_prefijo(p, m)

    # Mientras que i se encuentre dentro de p.
    while i < n:
        if p[j] == t[i]:
            # Si el caracter en p[j] es igual que t[i].
            # Verifica el proximo caracter en el patron y el texto.
            i += 1
            j += 1

        if j == m:
            # Si el index en j es igual que la longitud del patron,
            # hay una ocurrencia.
            yield i - j

            # El index j se mueve a la de la ocurrencia.
            j = lps[j - 1]

        elif i < n and p[j] != t[i]:
            # En otro caso, si i es menor que la longitud del texto y
            # el caracter en p[j] es distinto de t[i].
            if j != 0:
                # Si j es distinto de 0.
                # j se mueve a lsp[j - 1]
                j = lps[j - 1]

            else:
                # Sino i aumenta en uno.
                i += 1


# Funcion de prefijo.
def funcion_prefijo(p, m):
    # Se inicializa un arreglo con la longitud de los sufijos en 0.
    lps = [0] * m

    # Se inicializa la longitud del sufijo actual en 0.
    longitud_prefijo = 0

    # Se inicializa el analisis desde el segundo elemento.
    i = 1
    while i < m:
        if p[longitud_prefijo] == p[i]:
            # Si el caracter anterior es igual al actual la longitud del
            # sufijo aumenta en 1.
            longitud_prefijo += 1

            # Se agrega la longitud actual contada en el arreglo de
            # longitudes.
            lps[i] = longitud_prefijo

            # Se mueve una posicion en el patron.
            i += 1

        else:
            # Si los caracteres son distintos.
            if longitud_prefijo != 0:
                # Si la longitud del sufijo es distinta de cero, se compara
                # con el caracter anterior, hasta llegar al primer caracter
                # del sufijo.
                longitud_prefijo = lps[longitud_prefijo - 1]

            else:
                # Si se llega al ultimo caracter del sufijo y no se encuentra
                # un caracter similar, se reinicia el sufijo.
                lps[i] = 0

                # Se mueve al siguiente caracter en el patron.
                i += 1

    return lps
