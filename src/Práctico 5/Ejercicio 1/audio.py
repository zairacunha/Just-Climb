
from pathlib import Path

import pygame


CARPETA_SONIDOS = (
    # Guarda la ruta de la carpeta de sonidos del proyecto para poder cargar efectos y música.
    Path(__file__).resolve().parent.parent / "assets" / "sounds"
)


class Audio:
    def __init__(self):
        self.disponible = False  # Indica si el sistema de audio quedó inicializado correctamente.
        self.sonidos = {}  # Almacena los efectos de sonido cargados por nombre.

        try:
            pygame.mixer.init()  # Inicializa el mixer de audio de Pygame.
            self.disponible = True  # Marca el audio como disponible si la inicialización fue exitosa.
        except pygame.error as error:
            print(f"Audio desactivado: {error}")  # Muestra el motivo por el que no se pudo activar el audio.
            return  # Sale del constructor si el mixer no está disponible.

        # Los efectos de sonido se cargan una sola vez al iniciar el juego.
        archivos = {
            "punto": ("punto.wav", 0.65),
            "choque": ("choque.wav", 0.7),
            "game_over": ("game_over.wav", 0.8),
        }

        for nombre, (archivo, volumen) in archivos.items():
            ruta = CARPETA_SONIDOS / archivo  # Construye la ruta completa del archivo de sonido.

            if ruta.is_file():
                try:
                    sonido = pygame.mixer.Sound(str(ruta))  # Crea un objeto de sonido a partir del archivo.
                    sonido.set_volume(volumen)  # Ajusta el volumen del efecto para su uso en el juego.
                    self.sonidos[nombre] = sonido  # Guarda el sonido en el diccionario para reutilizarlo luego.
                except pygame.error as error:
                    print(f"No se pudo cargar {archivo}: {error}")  # Informa si un efecto no pudo cargarse.

        # La música se carga y se inicia en bucle si el archivo existe.
        ruta_musica = CARPETA_SONIDOS / "musica.ogg"  # Busca la pista de fondo dentro de la carpeta de sonidos.

        if ruta_musica.is_file():
            try:
                pygame.mixer.music.load(str(ruta_musica))  # Carga la música desde la ruta indicada.
                pygame.mixer.music.set_volume(0.25)  # Reduce el volumen de la música para no tapar los efectos.
                pygame.mixer.music.play(-1)  # Reproduce la música en bucle infinito.
            except pygame.error as error:
                print(f"No se pudo cargar la música: {error}")  # Muestra el error si la música no puede cargarse.

    def reproducir(self, nombre):
        sonido = self.sonidos.get(nombre)  # Busca el efecto de sonido solicitado por su nombre.
        if sonido is not None:
            sonido.play()  # Reproduce el efecto de sonido si fue cargado correctamente.

    def detener_musica(self):
        if self.disponible:
            pygame.mixer.music.stop()  # Detiene la reproducción de la música de fondo si el audio está disponible.
