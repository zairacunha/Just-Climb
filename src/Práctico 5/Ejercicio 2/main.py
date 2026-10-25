
import random

import pygame

from audio import Audio
from hud import dibujar_hud


# Define el tamaño de la ventana.
ANCHO = 800
ALTO = 600

# Las velocidades se expresan en píxeles por segundo.
VELOCIDAD_JUGADOR = 300
INTERVALO_ENEMIGOS = 1.5


class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Crea una superficie azul para representar al jugador.
        self.image = pygame.Surface((50, 50))
        self.image.fill((40, 180, 255))

        # Coloca al jugador cerca de la parte inferior de la ventana.
        self.rect = self.image.get_rect(
            center=(ANCHO // 2, ALTO - 70)
        )

        # Guarda la posición con decimales para que delta time
        # mantenga un movimiento fluido.
        self.posicion = pygame.Vector2(self.rect.topleft)

    def update(self, dt, teclas):
        # Empieza sin movimiento y modifica la dirección según las teclas.
        direccion = pygame.Vector2(0, 0)

        if teclas[pygame.K_LEFT]:
            direccion.x -= 1
        if teclas[pygame.K_RIGHT]:
            direccion.x += 1
        if teclas[pygame.K_UP]:
            direccion.y -= 1
        if teclas[pygame.K_DOWN]:
            direccion.y += 1

        # Evita que el jugador se mueva más rápido en diagonal.
        if direccion.length_squared() > 0:
            direccion = direccion.normalize()

        # Actualiza la posición usando velocidad y tiempo transcurrido.
        self.posicion += direccion * VELOCIDAD_JUGADOR * dt
        self.rect.topleft = (
            round(self.posicion.x),
            round(self.posicion.y),
        )

        # Impide que el jugador salga de la ventana.
        self.rect.clamp_ip(pygame.Rect(0, 0, ANCHO, ALTO))

        # Sincroniza la posición precisa con el rectángulo limitado.
        self.posicion = pygame.Vector2(self.rect.topleft)


class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Crea un cuadrado rojo para representar al enemigo.
        self.image = pygame.Surface((40, 40))
        self.image.fill((230, 55, 55))

        # El enemigo aparece en una posición horizontal aleatoria,
        # un poco por encima de la ventana.
        posicion_x = random.randint(0, ANCHO - self.image.get_width())
        posicion_y = random.randint(-100, -40)
        self.rect = self.image.get_rect(topleft=(posicion_x, posicion_y))

        # Cada enemigo cae a una velocidad aleatoria.
        self.posicion_y = float(self.rect.y)
        self.velocidad = random.randint(120, 260)

    def update(self, dt, teclas=None):
        # Mueve al enemigo hacia abajo usando delta time.
        self.posicion_y += self.velocidad * dt
        self.rect.y = round(self.posicion_y)

        # Elimina al enemigo cuando sale completamente por abajo.
        if self.rect.top > ALTO:
            self.kill()


def main():
    # Inicializa Pygame antes de crear la ventana y cargar el audio.
    pygame.init()

    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Ejercicio 2 - Timer y HUD")

    # El reloj limita los FPS y permite calcular delta time.
    reloj = pygame.time.Clock()
    fuente_hud = pygame.font.Font(None, 32)
    fuente_game_over = pygame.font.Font(None, 64)

    # Carga los sonidos y la música una sola vez al iniciar.
    audio = Audio()

    # Crea el jugador y los grupos de sprites.
    jugador = Jugador()
    todos_los_sprites = pygame.sprite.Group(jugador)
    enemigos = pygame.sprite.Group()

    # Inicializa el timer, el tiempo de partida y las vidas.
    timer_spawn = 0.0
    tiempo_transcurrido = 0.0
    vidas = 3
    game_over = False
    ejecutando = True

    # Bucle principal del juego.
    while ejecutando:
        # Convierte el tiempo del cuadro a segundos.
        dt = reloj.tick(60) / 1000.0

        # Revisa si el usuario cerró la ventana.
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        # Actualiza el juego mientras todavía haya vidas.
        if not game_over:
            tiempo_transcurrido += dt
            teclas = pygame.key.get_pressed()

            # Acumula tiempo y crea un enemigo cada 1,5 segundos.
            timer_spawn += dt

            while timer_spawn >= INTERVALO_ENEMIGOS:
                timer_spawn -= INTERVALO_ENEMIGOS

                enemigo = Enemigo()
                enemigos.add(enemigo)
                todos_los_sprites.add(enemigo)

            # Actualiza el movimiento del jugador y los enemigos.
            todos_los_sprites.update(dt, teclas)

            # Detecta los enemigos que chocaron con el jugador.
            # dokill=True elimina de los grupos a los enemigos que chocan.
            colisiones = pygame.sprite.spritecollide(
                jugador,
                enemigos,
                True,
            )

            # Cada cuadro con una o más colisiones quita una vida.
            if colisiones:
                vidas -= 1
                audio.reproducir_choque()

                # Termina la partida cuando las vidas llegan a cero.
                if vidas <= 0:
                    vidas = 0
                    game_over = True
                    audio.reproducir_game_over()
                    print("¡Game Over!")

        # El puntaje aumenta diez puntos por segundo sobrevivido.
        puntaje = int(tiempo_transcurrido * 10)

        # Dibuja primero el fondo y todos los sprites.
        pantalla.fill((30, 30, 30))
        todos_los_sprites.draw(pantalla)

        # Muestra el mensaje final cuando se terminan las vidas.
        if game_over:
            texto_game_over = fuente_game_over.render(
                "¡Game Over!",
                True,
                (255, 90, 90),
            )
            pantalla.blit(
                texto_game_over,
                texto_game_over.get_rect(
                    center=(ANCHO // 2, ALTO // 2)
                ),
            )

        # Dibuja el HUD al final, en coordenadas fijas de pantalla.
        dibujar_hud(
            pantalla,
            fuente_hud,
            puntaje,
            vidas,
            tiempo_transcurrido,
        )

        # Actualiza la ventana con todo lo dibujado en este cuadro.
        pygame.display.flip()

    # Detiene la música y cierra Pygame al salir.
    audio.detener_musica()
    pygame.quit()


if __name__ == "__main__":
    main()
