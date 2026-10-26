
from pathlib import Path # Importa la clase Path del módulo pathlib para trabajar con rutas de archivos y directorios de manera más sencilla y legible.

import pygame # Importa la biblioteca Pygame, que se utiliza para crear videojuegos y aplicaciones multimedia en Python.

class Jugador(pygame.sprite.Sprite): # Define la clase Jugador, que hereda de pygame.sprite.Sprite, lo que permite utilizar las funcionalidades de los sprites en Pygame.
    
    def __init__(self, ancho_ventana, alto_ventana): # Define el método constructor de la clase Jugador, que se ejecuta al crear una instancia de la clase. Recibe como parámetros el ancho y alto de la ventana del juego.
        
        super().__init__() # Llama al constructor de la clase base (pygame.sprite.Sprite) para inicializar correctamente la instancia de Jugador.

        ruta_imagen = (

            Path(__file__).resolve().parent.parent

            / "assets"

            / "images"

            / "jugador.png"
        )

        if ruta_imagen.exists():

            self.image = pygame.image.load(str(ruta_imagen)).convert_alpha() # Carga la imagen del jugador desde la ruta especificada y la convierte a un formato que permite transparencia (alpha channel) para que se vea correctamente en el juego.

            self.image = pygame.transform.scale(self.image, (50, 50)) # Escala la imagen del jugador a un tamaño de 50x50 píxeles para que se ajuste al diseño del juego.

        else:

            # Imagen de reemplazo si no existe jugador.png

            self.image = pygame.Surface((50, 50), pygame.SRCALPHA) # Crea una superficie transparente de 50x50 píxeles como imagen de reemplazo si no se encuentra el archivo jugador.png.

            self.image.fill((0, 200, 255)) # Rellena la superficie con un color azul (RGB: 0, 200, 255) para que el jugador sea visible en el juego.

        self.rect = self.image.get_rect(

            center=(ancho_ventana // 2, alto_ventana // 2) # Establece el rectángulo delimitador (rect) del jugador, que se utiliza para detectar colisiones y posicionar el sprite en la ventana del juego. El centro del rectángulo se coloca en el centro de la ventana del juego, utilizando el ancho y alto proporcionados como parámetros.

        )

        self.limites = pygame.Rect(0, 0, ancho_ventana, alto_ventana) # Define un rectángulo que representa los límites de la ventana del juego, para evitar que el jugador se mueva fuera de la pantalla.

        self.posicion = pygame.Vector2(self.rect.center) # Crea un vector de posición (posicion) que representa la ubicación actual del jugador en el espacio del juego, utilizando el centro del rectángulo delimitador como punto de referencia.

        self.velocidad = 300  # píxeles por segundo

    def update(self, dt, teclas):

        direccion = pygame.Vector2(0, 0) # Crea un vector de dirección (direccion) que se utilizará para determinar hacia dónde se moverá el jugador en función de las teclas presionadas.

        if teclas[pygame.K_LEFT]:

            direccion.x -= 1 # Si la tecla de flecha izquierda (K_LEFT) está presionada, se decrementa el valor de la componente x del vector de dirección en 1, lo que indica que el jugador se moverá hacia la izquierda.

        if teclas[pygame.K_RIGHT]:

            direccion.x += 1 # Si la tecla de flecha derecha (K_RIGHT) está presionada, se incrementa el valor de la componente x del vector de dirección en 1, lo que indica que el jugador se moverá hacia la derecha.

        if teclas[pygame.K_UP]:

            direccion.y -= 1 # Si la tecla de flecha arriba (K_UP) está presionada, se decrementa el valor de la componente y del vector de dirección en 1, lo que indica que el jugador se moverá hacia arriba.

        if teclas[pygame.K_DOWN]:

            direccion.y += 1 # Si la tecla de flecha abajo (K_DOWN) está presionada, se incrementa el valor de la componente y del vector de dirección en 1, lo que indica que el jugador se moverá hacia abajo.

        # Evita que moverse en diagonal sea más rápido.
        if direccion.length_squared() > 0:

            direccion = direccion.normalize() # Normaliza el vector de dirección para que tenga una longitud de 1, lo que evita que el jugador se mueva más rápido al moverse en diagonal (ya que la suma de las componentes x e y sería mayor que 1).

        self.posicion += direccion * self.velocidad * dt # Actualiza la posición del jugador sumando el vector de dirección multiplicado por la velocidad y el tiempo transcurrido (dt), lo que permite un movimiento suave y consistente en función del tiempo.

        self.rect.center = self.posicion # Actualiza el centro del rectángulo delimitador del jugador para que coincida con la nueva posición calculada, lo que asegura que la representación visual del jugador se mantenga alineada con su posición lógica en el juego.

        # Mantiene al jugador dentro de la ventana.

        self.rect.clamp_ip(self.limites) # Ajusta el rectángulo delimitador del jugador para que permanezca dentro de los límites de la ventana del juego, evitando que se salga de la pantalla.

        self.posicion = pygame.Vector2(self.rect.center) # Actualiza la posición del jugador para que coincida con el centro del rectángulo delimitador después de aplicar los límites, asegurando que la posición lógica del jugador esté siempre dentro de la ventana del juego.
