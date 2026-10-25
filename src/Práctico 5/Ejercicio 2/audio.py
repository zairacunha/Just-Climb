
from pathlib import Path

import pygame


# Como audio.py está directamente dentro de "Ejercicio 2",
# buscamos la carpeta sounds dentro de Ejercicio 2/assets.
CARPETA_SONIDOS = (
    Path(__file__).resolve().parent / "assets" / "sounds"
)


class Audio:
    def __init__(self):
        # Los sonidos empiezan vacíos por si no existen los archivos
        # o si el sistema no puede inicializar el audio.
        self.disponible = False
        self.sonido_punto = None
        self.sonido_choque = None
        self.sonido_game_over = None

        # Inicia el mixer solamente si todavía no estaba iniciado.
        # El juego puede continuar aunque el audio no esté disponible.
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init()

            self.disponible = True
        except pygame.error as error:
            print(f"No se pudo iniciar el audio: {error}")
            return

        # Construye una ruta para cada efecto de sonido.
        ruta_punto = CARPETA_SONIDOS / "punto.wav"
        ruta_choque = CARPETA_SONIDOS / "choque.wav"
        ruta_game_over = CARPETA_SONIDOS / "game_over.wav"

        # Carga el efecto de punto una sola vez.
        # Queda disponible si luego agregas monedas o puntos al juego.
        if ruta_punto.is_file():
            try:
                self.sonido_punto = pygame.mixer.Sound(str(ruta_punto))
                self.sonido_punto.set_volume(0.65)
            except pygame.error as error:
                print(f"No se pudo cargar punto.wav: {error}")
        else:
            print(f"No se encontró el archivo: {ruta_punto}")

        # Carga el efecto que suena cuando el jugador choca con un enemigo.
        if ruta_choque.is_file():
            try:
                self.sonido_choque = pygame.mixer.Sound(str(ruta_choque))
                self.sonido_choque.set_volume(0.7)
            except pygame.error as error:
                print(f"No se pudo cargar choque.wav: {error}")
        else:
            print(f"No se encontró el archivo: {ruta_choque}")

        # Carga el efecto que suena cuando se terminan las vidas.
        if ruta_game_over.is_file():
            try:
                self.sonido_game_over = pygame.mixer.Sound(
                    str(ruta_game_over)
                )
                self.sonido_game_over.set_volume(0.8)
            except pygame.error as error:
                print(f"No se pudo cargar game_over.wav: {error}")
        else:
            print(f"No se encontró el archivo: {ruta_game_over}")

        # La música es opcional para el funcionamiento del programa.
        ruta_musica = CARPETA_SONIDOS / "musica.ogg"

        if ruta_musica.is_file():
            try:
                pygame.mixer.music.load(str(ruta_musica))
                pygame.mixer.music.set_volume(0.25)
                pygame.mixer.music.play(-1)  # -1 hace que se repita en bucle.
            except pygame.error as error:
                print(f"No se pudo cargar musica.ogg: {error}")
        else:
            print(f"No se encontró la música: {ruta_musica}")

    def reproducir_punto(self):
        # Reproduce el sonido solo si se cargó correctamente.
        if self.sonido_punto is not None:
            self.sonido_punto.play()

    def reproducir_choque(self):
        # Reproduce el sonido cuando el jugador pierde una vida.
        if self.sonido_choque is not None:
            self.sonido_choque.play()

    def reproducir_game_over(self):
        # Reproduce el sonido cuando el juego termina.
        if self.sonido_game_over is not None:
            self.sonido_game_over.play()

    def detener_musica(self):
        # Detiene la música al cerrar el juego.
        if self.disponible:
            try:
                pygame.mixer.music.stop()
            except pygame.error:
                pass
