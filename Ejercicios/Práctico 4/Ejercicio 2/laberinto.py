
import pygame


TAM_CELDA = 40 # Tamaño de cada celda en píxeles.

# 1 = pared, 0 = camino.

# Este mapa tiene 21 columnas y 17 filas.

MAPA = [
    "1" * 21, # Fila superior
    "1" + "0" * 19 + "1", # Fila 1
    "1" + "1" * 18 + "0" + "1", # Fila 2
    "1" + "0" * 19 + "1", # Fila 3
    "1" + "0" + "1" * 18 + "1", # Fila 4
    "1" + "0" * 19 + "1", # Fila 5
    "1" + "1" * 18 + "0" + "1", # Fila 6
    "1" + "0" * 19 + "1", # Fila 7
    "1" + "0" + "1" * 18 + "1", # Fila 8
    "1" + "0" * 19 + "1", # Fila 9
    "1" + "1" * 18 + "0" + "1", # Fila 10
    "1" + "0" * 19 + "1", # Fila 11
    "1" + "0" + "1" * 18 + "1", # Fila 12
    "1" + "0" * 19 + "1", # Fila 13
    "1" + "1" * 18 + "0" + "1", # Fila 14
    "1" + "0" * 19 + "1", # Fila 15
    "1" * 21, # Fila inferior
] # Mapa del juego

COLUMNAS = len(MAPA[0]) # Número de columnas en el mapa.

FILAS = len(MAPA) # Número de filas en el mapa.

if any(len(fila) != COLUMNAS for fila in MAPA):

    raise ValueError("Todas las filas del mapa deben tener el mismo ancho.")

ANCHO_MUNDO = COLUMNAS * TAM_CELDA # Ancho del mundo en píxeles.

ALTO_MUNDO = FILAS * TAM_CELDA # Alto del mundo en píxeles.


def construir_paredes():

    paredes = [] # Lista para almacenar los rectángulos de las paredes.

    for fila, contenido in enumerate(MAPA):

        for columna, celda in enumerate(contenido):

            if celda == "1":

                pared = pygame.Rect(
                    
                    columna * TAM_CELDA, # Posición X de la pared
                    fila * TAM_CELDA, # Posición Y de la pared
                    TAM_CELDA, # Ancho de la pared
                    TAM_CELDA, # Alto de la pared
                ) # Rectángulo de la pared

                paredes.append(pared) # Agrega el rectángulo de la pared a la lista de paredes.

    return paredes # Devuelve la lista de rectángulos de las paredes.


PAREDES = construir_paredes() # Lista de rectángulos que representan las paredes del mapa.

# Meta ubicada en la esquina inferior derecha del camino.
META = pygame.Rect(
    (COLUMNAS - 2) * TAM_CELDA + 8, # Posición X de la meta
    (FILAS - 2) * TAM_CELDA + 8, # Posición Y de la meta
    24, # Ancho de la meta
    24, # Alto de la meta
) # Rectángulo de la meta
