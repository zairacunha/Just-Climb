
import pygame


def dibujar_hud(pantalla, fuente, puntaje, vidas, tiempo):
    # Usa el ancho actual de la ventana para colocar los textos.
    ancho_pantalla = pantalla.get_width()

    # Crea cada texto del HUD con su color correspondiente.
    texto_puntaje = fuente.render(
        f"Puntaje: {puntaje}",
        True,
        (255, 255, 255),
    )
    texto_vidas = fuente.render(
        f"Vidas: {vidas}",
        True,
        (255, 120, 120),
    )
    texto_tiempo = fuente.render(
        f"Tiempo: {int(tiempo)}",
        True,
        (255, 255, 120),
    )

    # Dibuja el HUD en coordenadas de pantalla, no del mundo.
    # Por eso sus posiciones no cambian con el movimiento del juego.
    pantalla.blit(texto_puntaje, (10, 10))
    pantalla.blit(
        texto_vidas,
        (ancho_pantalla - texto_vidas.get_width() - 10, 10),
    )
    pantalla.blit(
        texto_tiempo,
        (ancho_pantalla // 2 - texto_tiempo.get_width() // 2, 10),
    )
