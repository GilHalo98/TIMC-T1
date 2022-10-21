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
    log = ''

    n = len(t)
    m = len(p)

    log += '\nlongitud del texto {}'.format(n)
    log += '\nlongitud del patron {}'.format(m)

    i = m - 1
    j = m - 1

    while True:
        # Compara el caracter en P[j] con el de T[i]
        log += '\nse compara P[{}] = {} con T[{}] = {}'.format(j, p[j], i, t[i])
        if p[j] == t[i]:
            log += '\nlos caracters son similares'
            if j == 0:
                log += '\nse alcanzo el final del patron'
                log += '\nel patron se contro en el texto desde el index i = {} hasta i = {}'.format(i, i + m)
                # Se comprueba la comparacion del ultimo caracter del
                # patron, el patron se encuentra en el texto.
                yield i

                i += (m * 2) - 1
                log += '\nnos movemos a i {}'.format(i)
                j = m - 1
                log += '\nreseteamos j = {}'.format(j)
            else:
                # Mueve la comparacion al siguiente caracter.
                i -= 1
                j -= 1
                log += '\nmovemos la comparacion a i {} y j {}'.format(i, j)
        else:
            # La comparacion fallo, se salta m caracteres a la derecha
            # en T.
            log += '\nson caracteres distintos'

            log += '\nbuscamos la ultima ocurrencia de un prefijo en el texto'
            ocurrencia_izquierda, log_last = last(t[i], p, m)
            log += log_last
            log += '\nla ocurrencia se encuentra en i = {}'.format(ocurrencia_izquierda)

            log += '\n nos movemos al minimo entre j y el index de la ocurrencia'
            i += m - min(j, 1 + ocurrencia_izquierda)

            # Se reinicia la comparacion desde P[m - 1]
            j = m - 1
            log += '\nreseteamos j = {}'.format(j)

        if i > n - 1:
            log += '\nhemos alcanzado el final del texto'
            break

    print(log)


# Retorna el primer index encontrado del elemento x, desde
# la derecha hacia la izquierda en el patron.
def last(c, p, m, log=''):
    i = m - 1
    log += '\nempezamos en i = {}'.format(i)
    log += '\nultima ocurrencia es C = {}'.format(c)
    while i >= 0:
        log += '\ncomparando P[{}] = {} con {}'.format(i, p[i], c)
        if p[i] == c:
            log += '\nse encontro una ocurrencia en i = {}'.format(i)
            break
        else:
            log += ', es distinto'
        i -= 1
        log += '\nnos movemos a i = {}'.format(i)
    return i, log


# Retorna el minimo entre dos datos.
def min(a, b):
    return a if a < b else b


# Algoritmo de Knuth-Morres-Pratt.
def kmp(t, p):
    log = ''
    n = len(t)  # Longitud del texto.
    m = len(p)  # Longitud del patron.

    log += '\nlongitud del texto {}'.format(n)
    log += '\nlongitud del patron {}'.format(m)

    j = 0  # Index del patron.
    i = 0  # Index del texto.

    # Precomputa el arreglo de lps.
    lps = funcion_prefijo(p, m)

    iter = 0

    # Mientras que i se encuentre dentro de p.
    while i < n:
        log += '\niteracion {}: se compara P[{}] = {} con T[{}] = {}'.format(iter, j, p[j], i, t[i])
        if p[j] == t[i]:
            log += '\n\tlos caracters son similares'
            # Si el caracter en p[j] es igual que t[i].
            # Verifica el proximo caracter en el patron y el texto.
            i += 1
            j += 1
            log += '\n\tnos movemos a i = {} y j = {}'.format(i, j)

        if j == m:
            # Si el index en j es igual que la longitud del patron,
            # hay una ocurrencia.
            log += '\n\t----| hay una coinciencia en i = {} hasta i = {}'.format(i - j, i - 1)
            yield i - j

            # El index j se mueve a la de la ocurrencia.
            j = lps[0]
            i += 1
            log += '\n\tnos movemos a i = {} y j = {}'.format(i, j)

        elif i < n and p[j] != t[i]:
            log += '\n\ti es menor que n y el caracer en P[{}] = {} es distinto de T[{}] = {}'.format(
                j,
                p[j],
                i,
                t[i]
            )
            # En otro caso, si i es menor que la longitud del texto y
            # el caracter en p[j] es distinto de t[i].
            if j != 0:
                # Si j es distinto de 0.
                # j se mueve a lsp[j - 1]
                j = lps[j - 1]
                log += '\n\t\tnos movemos a j = {}'.format(j)

            else:
                # Sino i aumenta en uno.
                i += 1
                log += '\n\t\tnos movemos a i = {}'.format(i)
        iter += 1
    print(log)


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
