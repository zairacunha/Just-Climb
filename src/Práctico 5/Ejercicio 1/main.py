
import random

import pygame

from audio import Audio


ANCHO = 800  # Ancho de la ventana del juego.
ALTO = 600  # Alto de la ventana del juego.
VELOCIDAD = 300  # Velocidad de desplazamiento del jugador en píxeles por segundo.


def main():
    pygame.init()  # Inicializa todos los módulos de Pygame.

    pantalla = pygame.display.set_mode((ANCHO, ALTO))  # Crea la ventana principal del juego.
    pygame.display.set_caption("Ejercicio 1 - Sonido y música")  # Define el título de la ventana.

    reloj = pygame.time.Clock()  # Controla el tiempo del juego para mantener una tasa de fotogramas estable.
    fuente = pygame.font.Font(None, 32)  # Fuente utilizada para mostrar el puntaje.
    audio = Audio()  # Crea el objeto encargado de gestionar sonidos y música.

    jugador = pygame.Rect(100, 100, 50, 50)  # Rectángulo que representa al personaje controlado por el jugador.
    posicion_jugador = pygame.Vector2(jugador.topleft)  # Guarda la posición exacta del jugador con coordenadas flotantes.

    objetivo = pygame.Rect(0, 0, 36, 36)  # Rectángulo que representa el objetivo a recoger.
    objetivo.center = (
        random.randint(18, ANCHO - 18),
        random.randint(18, ALTO - 18),
    )  # Coloca el objetivo en una posición aleatoria dentro de la pantalla.

    puntaje = 0  # Acumula la cantidad de objetivos recogidos.
    ejecutando = True  # Controla el ciclo principal del juego.

    while ejecutando:
        dt = reloj.tick(60) / 1000.0  # Calcula el tiempo transcurrido entre frames para mover al jugador de forma uniforme.

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Si el usuario cierra la ventana, termina el juego.
                ejecutando = False

        teclas = pygame.key.get_pressed()  # Obtiene el estado de todas las teclas del teclado.
        direccion = pygame.Vector2(0, 0)  # Vector que representa la dirección del movimiento del jugador.

        if teclas[pygame.K_LEFT]:
            direccion.x -= 1  # Mueve al jugador hacia la izquierda.
        if teclas[pygame.K_RIGHT]:
            direccion.x += 1  # Mueve al jugador hacia la derecha.
        if teclas[pygame.K_UP]:
            direccion.y -= 1  # Mueve al jugador hacia arriba.
        if teclas[pygame.K_DOWN]:
            direccion.y += 1  # Mueve al jugador hacia abajo.

        if direccion.length_squared() > 0:
            direccion = direccion.normalize()  # Normaliza el vector para que el movimiento tenga velocidad constante.

        posicion_jugador += direccion * VELOCIDAD * dt  # Actualiza la posición con la velocidad y el tiempo.
        jugador.topleft = (round(posicion_jugador.x), round(posicion_jugador.y))  # Redondea la posición para convertirla a enteros.
        jugador.clamp_ip(pantalla.get_rect())  # Mantiene al jugador dentro de los límites de la ventana.
        posicion_jugador = pygame.Vector2(jugador.topleft)  # Guarda la posición actualizada en el vector.

        if jugador.colliderect(objetivo):
            puntaje += 1  # Incrementa el puntaje cuando el jugador toca el objetivo.
            audio.reproducir("punto")  # Reproduce el efecto de sonido de punto.
            objetivo.center = (
                random.randint(18, ANCHO - 18),
                random.randint(18, ALTO - 18),
            )  # Genera una nueva posición para el objetivo.

        pantalla.fill((30, 30, 30))  # Rellena la pantalla con un fondo oscuro.
        pygame.draw.rect(pantalla, (40, 180, 255), jugador)  # Dibuja al jugador como un rectángulo azul.
        pygame.draw.circle(pantalla, (255, 210, 40), objetivo.center, 18)  # Dibuja el objetivo como un círculo amarillo.

        texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))  # Crea la imagen del texto del puntaje.
        pantalla.blit(texto, (10, 10))  # Muestra el puntaje en la parte superior izquierda.

        pygame.display.flip()  # Actualiza la pantalla con todo lo dibujado.

    audio.detener_musica()  # Detiene la música de fondo al salir del juego.
    pygame.quit()  # Cierra correctamente Pygame.


if __name__ == "__main__":
    main()  # Ejecuta la función principal cuando se corre el archivo.
