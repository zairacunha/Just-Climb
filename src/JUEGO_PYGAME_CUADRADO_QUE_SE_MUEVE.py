import pygame

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Cuadrado con flechas")

FONDO = (30, 30, 30)
COLOR_JUGADOR = (50, 180, 255)
BLANCO = (255, 255, 255)

jugador = pygame. Rect(375, 275, 50, 50)
velocidad = 300  # píxeles por segundo

fuente = pygame.font. Font(None, 30)
clock = pygame.time. Clock()
ejecutando = True

while ejecutando:
    # dt expresa el tiempo transcurrido desde el último fotograma, en segundos.
    dt = clock.tick(60) / 1000

    for evento in pygame.event.get():
        if evento.type == pygame. QUIT:
            ejecutando = False

    teclas = pygame.key.get_pressed()
    direccion = pygame. Vector2(0, 0)

    if teclas[pygame. K_LEFT]:
        direccion.x -= 1
    if teclas[pygame. K_RIGHT]:
        direccion.x += 1
    if teclas[pygame. K_UP]:
        direccion.y -= 1
    if teclas[pygame. K_DOWN]:
        direccion.y += 1

    # Normaliza el movimiento diagonal.
    if direccion.length_squared() > 0:
        direccion = direccion.normalize()

    jugador.x += direccion.x * velocidad * dt
    jugador.y += direccion.y * velocidad * dt

    # Mantiene el cuadrado dentro de la ventana.
    jugador.clamp_ip(pantalla.get_rect())

    pantalla.fill(FONDO)
    pygame.draw.rect(pantalla, COLOR_JUGADOR, jugador)

    fps_texto = fuente.render(
        f"FPS: {int(clock.get_fps())}", True, BLANCO
    )
    pantalla.blit(fps_texto, (10, 10))

    pygame.display.flip()

pygame.quit()
