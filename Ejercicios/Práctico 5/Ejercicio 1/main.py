
import random

import pygame

from audio import Audio


# Define el tamaño de la ventana del juego.
ANCHO = 800
ALTO = 600

# Define el tamaño y la velocidad del jugador.
TAM_JUGADOR = 50
VELOCIDAD_JUGADOR = 300

# Define el tamaño del objetivo que el jugador debe recoger.
TAM_OBJETIVO = 36


def colocar_objetivo(objetivo, jugador):
    # Elige una posición aleatoria dentro de la ventana.
    # Si el objetivo aparece sobre el jugador, vuelve a elegirla.
    while True:
        objetivo.center = (
            random.randint(TAM_OBJETIVO // 2, ANCHO - TAM_OBJETIVO // 2),
            random.randint(TAM_OBJETIVO // 2, ALTO - TAM_OBJETIVO // 2),
        )

        if not objetivo.colliderect(jugador):
            break


def main():
    # Inicializa Pygame antes de crear la ventana y el sistema de audio.
    pygame.init()

    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Ejercicio 1 - Sonido y música")

    # El reloj controla los FPS y permite calcular delta time.
    reloj = pygame.time.Clock()
    fuente = pygame.font.Font(None, 32)

    # Crea el sistema de audio una sola vez, fuera del bucle principal.
    audio = Audio()

    # Crea al jugador y guarda su posición con decimales
    # para que el movimiento con delta time sea más preciso.
    jugador = pygame.Rect(100, 100, TAM_JUGADOR, TAM_JUGADOR)
    posicion_jugador = pygame.Vector2(jugador.topleft)

    # Crea el objetivo y lo coloca en una posición aleatoria.
    objetivo = pygame.Rect(0, 0, TAM_OBJETIVO, TAM_OBJETIVO)
    colocar_objetivo(objetivo, jugador)

    puntaje = 0
    ejecutando = True

    # Bucle principal: procesa eventos, actualiza el juego y dibuja la pantalla.
    while ejecutando:
        # Convierte el tiempo transcurrido del cuadro a segundos.
        dt = reloj.tick(60) / 1000.0

        # Comprueba si el jugador cerró la ventana.
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        # Lee las teclas presionadas para decidir hacia dónde mover al jugador.
        teclas = pygame.key.get_pressed()
        direccion = pygame.Vector2(0, 0)

        if teclas[pygame.K_LEFT]:
            direccion.x -= 1
        if teclas[pygame.K_RIGHT]:
            direccion.x += 1
        if teclas[pygame.K_UP]:
            direccion.y -= 1
        if teclas[pygame.K_DOWN]:
            direccion.y += 1

        # Normaliza la dirección para que el movimiento diagonal no sea más rápido que el movimiento horizontal o vertical.
        if direccion.length_squared() > 0:
            direccion = direccion.normalize()

        # Actualiza la posición según la velocidad y el tiempo transcurrido.
        posicion_jugador += direccion * VELOCIDAD_JUGADOR * dt
        jugador.topleft = (
            round(posicion_jugador.x),
            round(posicion_jugador.y),
        )

        # Mantiene al jugador dentro de los límites de la ventana.
        jugador.clamp_ip(pantalla.get_rect())

        # Sincroniza la posición precisa con el rectángulo después del límite.
        posicion_jugador = pygame.Vector2(jugador.topleft)

        # Al tocar el objetivo, suma un punto, reproduce el efecto
        # y coloca el objetivo en una nueva posición.
        if jugador.colliderect(objetivo):
            puntaje += 1
            audio.reproducir_punto()
            colocar_objetivo(objetivo, jugador)

        # Limpia la pantalla y dibuja el jugador y el objetivo.
        pantalla.fill((30, 30, 30))
        pygame.draw.rect(pantalla, (40, 180, 255), jugador)
        pygame.draw.rect(pantalla, (255, 210, 40), objetivo)

        # Muestra el puntaje en la esquina superior izquierda.
        texto_puntaje = fuente.render(
            f"Puntaje: {puntaje}",
            True,
            (255, 255, 255),
        )
        pantalla.blit(texto_puntaje, (10, 10))

        # Presenta en pantalla todo lo dibujado en este cuadro.
        pygame.display.flip()

    # Detiene la música y cierra Pygame al salir del bucle.
    audio.detener_musica()
    pygame.quit()


if __name__ == "__main__":
    main()
