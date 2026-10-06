import random
import pygame

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Recoger el objetivo")

FONDO = (30, 30, 30)
AZUL = (50, 120, 255)
ROJO = (230, 50, 50)
BLANCO = (255, 255, 255)

jugador = pygame. Rect(375, 275, 50, 50)
objetivo = pygame. Rect(0, 0, 40, 40)

def mover_objetivo():
    """Coloca el objetivo en una posición aleatoria que no toque al jugador."""
    while True:
        objetivo.x = random.randint(0, ANCHO - objetivo.width)
        objetivo.y = random.randint(0, ALTO - objetivo.height)
        if not jugador.colliderect(objetivo):
            break

mover_objetivo()

velocidad = 300  # píxeles por segundo
puntos = 0
fuente = pygame.font. Font(None, 32)
clock = pygame.time. Clock()
ejecutando = True

while ejecutando:
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

    # Normaliza la dirección para que el movimiento diagonal no sea más rápido.
    if direccion.length_squared() > 0:
        direccion = direccion.normalize()

    jugador.x += direccion.x * velocidad * dt
    jugador.y += direccion.y * velocidad * dt
    jugador.clamp_ip(pantalla.get_rect())

    if jugador.colliderect(objetivo):
        puntos += 1
        mover_objetivo()

    pantalla.fill(FONDO)
    pygame.draw.rect(pantalla, AZUL, jugador)
    pygame.draw.rect(pantalla, ROJO, objetivo)

    texto_puntos = fuente.render(f"Puntos: {puntos}", True, BLANCO)
    pantalla.blit(texto_puntos, (10, 10))

    pygame.display.flip()

pygame.quit()
