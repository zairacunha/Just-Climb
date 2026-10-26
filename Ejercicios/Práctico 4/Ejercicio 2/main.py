
import pygame

# Importa la clase que controla el movimiento de la cámara para seguir al jugador.
from camara import Camara

# Importa las constantes definidas en el archivo del laberinto.
from laberinto import (
    ALTO_MUNDO,
    ANCHO_MUNDO,
    META,
    PAREDES,
    TAM_CELDA,
)

# Dimensiones de la ventana del juego.
ANCHO_VENTANA = 640
ALTO_VENTANA = 480

# Tamaño del rectángulo del jugador y velocidad de movimiento.
TAM_JUGADOR = 24
VELOCIDAD_JUGADOR = 220


def leer_direccion(teclas):
    """
    Lee las teclas del teclado y calcula la dirección del movimiento del jugador.

    Parámetros:
        teclas: estado de todas las teclas del teclado, obtenido con pygame.key.get_pressed().

    Retorna:
        Un objeto pygame.Vector2 con la dirección normalizada del movimiento.
        Si no se presiona ninguna tecla, devuelve (0, 0).
    """
    # Se crea un vector de dos dimensiones para representar movimiento horizontal y vertical.
    # Se usa un valor de -1, 0 o 1 en cada eje para indicar el sentido del desplazamiento.
    direccion = pygame.Vector2(0, 0)

    # Si se presiona la flecha izquierda, se mueve hacia la izquierda en el eje X.
    if teclas[pygame.K_LEFT]:
        direccion.x -= 1
    # Si se presiona la flecha derecha, se mueve hacia la derecha en el eje X.
    if teclas[pygame.K_RIGHT]:
        direccion.x += 1
    # Si se presiona la flecha arriba, se mueve hacia arriba en el eje Y.
    if teclas[pygame.K_UP]:
        direccion.y -= 1
    # Si se presiona la flecha abajo, se mueve hacia abajo en el eje Y.
    if teclas[pygame.K_DOWN]:
        direccion.y += 1

    # Si hay alguna dirección activa, se normaliza el vector para que la velocidad total
    # no dependa de si se mueve en una sola dirección o en diagonal.
    if direccion.length_squared() > 0:
        direccion = direccion.normalize()

    return direccion


def mover_jugador(jugador, posicion, dx, dy, paredes):
    """
    Mueve al jugador en dos ejes y corrige las colisiones con las paredes.

    Parámetros:
        jugador: rectángulo del jugador representado por pygame.Rect.
        posicion: vector que guarda la posición real del jugador para controlar desplazamientos.
        dx: cantidad de movimiento en el eje X.
        dy: cantidad de movimiento en el eje Y.
        paredes: lista de rectángulos que representan los muros del laberinto.

    Descripción:
        Primero se mueve en X y comprueba si intersecta con alguna pared;
        si ocurre, lo empuja hacia afuera del muro en el eje correspondiente.
        Después hace lo mismo con Y para evitar que atraviese los muros.
    """
    # Movimiento horizontal: se actualiza la posición X y luego se prueba una colisión.
    if dx != 0:
        posicion.x += dx
        jugador.x = round(posicion.x)

        # Revisa cada pared para saber si el rectángulo del jugador quedó dentro de ella.
        for pared in paredes:
            if jugador.colliderect(pared):
                # Si el jugador se movió a la derecha, su lado derecho debe quedar
                # pegado al lado izquierdo de la pared para impedir pasar atravesándola.
                if dx > 0:
                    jugador.right = pared.left
                else:
                    jugador.left = pared.right

                # Se sincroniza la posición del vector con la nueva posición del rectángulo.
                posicion.x = jugador.x

    # Movimiento vertical: se aplica la misma lógica en Y.
    if dy != 0:
        posicion.y += dy
        jugador.y = round(posicion.y)

        for pared in paredes:
            if jugador.colliderect(pared):
                # Si se mueve hacia abajo, el borde inferior del jugador se queda
                # justo por encima de la pared.
                if dy > 0:
                    jugador.bottom = pared.top
                else:
                    jugador.top = pared.bottom

                posicion.y = jugador.y


def main():
    """
    Función principal del juego.

    Se encarga de inicializar pygame, crear la ventana, manejar eventos,
    actualizar la lógica del juego, dibujar cada frame y cerrar correctamente la aplicación.
    """
    # Inicializa todos los módulos de Pygame para poder usar ventanas, eventos, dibujo y audio.
    pygame.init()

    # Crea la ventana del juego con el ancho y alto definidos al inicio.
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Ejercicio 2 - Laberinto con scroll")

    # Reloj del juego para controlar la frecuencia de actualización del bucle principal.
    reloj = pygame.time.Clock()
    # Fuente usada para mostrar texto como "Flechas: mover" o "¡Ganaste!".
    fuente = pygame.font.Font(None, 32)

    # Se crea el rectángulo del jugador con tamaño fijo y posición inicial.
    # La posición inicial se coloca un poco dentro del laberinto para que no quede pegado a la pared.
    jugador = pygame.Rect(
        TAM_CELDA + (TAM_CELDA - TAM_JUGADOR) // 2,
        TAM_CELDA + (TAM_CELDA - TAM_JUGADOR) // 2,
        TAM_JUGADOR,
        TAM_JUGADOR,
    )
    # Guarda la posición exacta del jugador en un Vector2 para mejorar el movimiento continuo.
    posicion_jugador = pygame.Vector2(jugador.topleft)

    # Se crea la cámara del juego y se inicializan las variables del estado del juego.
    camara = Camara(ANCHO_VENTANA, ALTO_VENTANA)
    ganaste = False
    ejecutando = True

    # Bucle principal del juego: se repite hasta que el usuario cierre la ventana.
    while ejecutando:
        # dt representa el tiempo en segundos que pasó entre fotogramas.
        # Con esto, el movimiento del jugador es consistente aunque el juego corra a distinta velocidad.
        dt = reloj.tick(60) / 1000

        # Se procesan los eventos del juego, como cerrar la ventana o presionar teclas.
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        # Mientras no se haya ganado, el jugador puede moverse y actualizar la lógica del juego.
        if not ganaste:
            # Lee todas las teclas presionadas para decidir la dirección del movimiento.
            teclas = pygame.key.get_pressed()
            direccion = leer_direccion(teclas)

            # Calcula el desplazamiento real del personaje según la velocidad y el tiempo transcurrido.
            dx = direccion.x * VELOCIDAD_JUGADOR * dt
            dy = direccion.y * VELOCIDAD_JUGADOR * dt

            # Se mueve al jugador y se corrigen colisiones con paredes.
            mover_jugador(jugador, posicion_jugador, dx, dy, PAREDES)

            # Si el rectángulo del jugador toca la meta, se termina la partida y se muestra mensaje.
            if jugador.colliderect(META):
                ganaste = True
                print("¡Ganaste!")

        # La cámara sigue al jugador, pero se limita a los bordes del mapa para evitar
        # que se salga del área del laberinto.
        camara.seguir(jugador, ANCHO_MUNDO, ALTO_MUNDO)

        # Se limpia la pantalla con un fondo oscuro para dibujar el siguiente frame.
        pantalla.fill((30, 35, 45))

        # Dibuja cada pared del laberinto ajustando su posición con la cámara.
        for pared in PAREDES:
            pygame.draw.rect(
                pantalla,
                (105, 115, 130),
                camara.aplicar(pared),
            )

        # Dibuja la meta del nivel con el desplazamiento de la cámara.
        pygame.draw.rect(
            pantalla,
            (60, 220, 100),
            camara.aplicar(META),
        )

        # Dibuja al jugador con la posición ajustada por la cámara.
        pygame.draw.rect(
            pantalla,
            (40, 180, 255),
            camara.aplicar(jugador),
        )

        # Muestra un texto en la pantalla informando si el jugador ganó o si debe seguir moviéndose.
        texto = fuente.render(
            "¡Ganaste!" if ganaste else "Flechas: mover",
            True,
            (255, 255, 255),
        )
        pantalla.blit(texto, (10, 10))

        # Actualiza la pantalla para mostrar todos los cambios realizados en este frame.
        pygame.display.flip()

    # Se cierra correctamente Pygame al terminar el bucle.
    pygame.quit()


if __name__ == "__main__":
    # Esta línea permite ejecutar el archivo como script principal.
    main()
