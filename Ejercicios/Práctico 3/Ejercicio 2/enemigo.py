
import random # Importa el módulo random, que proporciona funciones para generar números aleatorios y realizar selecciones aleatorias. En este caso, se utilizará para determinar posiciones y velocidades aleatorias de los enemigos en el juego.

import pygame


class Enemigo(pygame.sprite.Sprite):

    def __init__(self, ancho_ventana, alto_ventana):

        super().__init__() # Llama al constructor de la clase base (pygame.sprite.Sprite) para inicializar correctamente la instancia de Enemigo.

        self.image = pygame.Surface((40, 40)) # Crea una superficie de 40x40 píxeles que representará la imagen del enemigo en el juego. Esta superficie se utilizará para dibujar el enemigo en la pantalla.

        self.image.fill((230, 50, 50)) # Rellena la superficie del enemigo con un color rojo (RGB: 230, 50, 50) para que sea visible en el juego. Este color se puede cambiar según las preferencias del desarrollador.

        self.rect = self.image.get_rect() # Obtiene el rectángulo delimitador (rect) de la superficie del enemigo, que se utilizará para detectar colisiones y posicionar el sprite en la ventana del juego. El rectángulo se ajusta automáticamente al tamaño de la superficie creada anteriormente.

        self.rect.x = random.randint(0, ancho_ventana - self.rect.width) # Asigna una posición horizontal aleatoria (x) al enemigo dentro de los límites de la ventana del juego. La función random.randint genera un número entero aleatorio entre 0 y el ancho de la ventana menos el ancho del rectángulo del enemigo, asegurando que el enemigo no se dibuje fuera de la pantalla.

        self.rect.y = random.randint(-100, -40) # Asigna una posición vertical aleatoria (y) al enemigo fuera de la parte superior de la ventana del juego. La función random.randint genera un número entero aleatorio entre -100 y -40, lo que permite que los enemigos aparezcan desde arriba y se desplacen hacia abajo en la pantalla.

        self.posicion = pygame.Vector2(self.rect.topleft) # Crea un vector de posición (posicion) que representa la ubicación actual del enemigo en el espacio del juego, utilizando la esquina superior izquierda del rectángulo delimitador como punto de referencia. Este vector se utilizará para actualizar la posición del enemigo de manera más precisa y fluida.

        self.velocidad = random.randint(100, 250) # Asigna una velocidad aleatoria al enemigo, que determinará qué tan rápido se moverá hacia abajo en la pantalla. La función random.randint genera un número entero aleatorio entre 100 y 250 píxeles por segundo, lo que permite que los enemigos tengan diferentes velocidades y aumente la dificultad del juego.

        self.alto_ventana = alto_ventana # Almacena la altura de la ventana del juego en la variable alto_ventana, que se utilizará para determinar cuándo el enemigo ha salido de la pantalla y debe ser eliminado del juego.

    def update(self, dt, teclas=None):

        self.posicion.y += self.velocidad * dt # Actualiza la posición vertical del enemigo en función de su velocidad y el tiempo transcurrido desde el último fotograma (dt). Esto permite que el enemigo se desplace hacia abajo en la pantalla de manera consistente, independientemente de la velocidad de procesamiento del sistema.

        self.rect.topleft = self.posicion # Actualiza la posición del rectángulo delimitador (rect) del enemigo para que coincida con la nueva posición calculada en el vector de posición (posicion). Esto asegura que el rectángulo se mueva junto con la imagen del enemigo y se mantenga sincronizado para la detección de colisiones.

        if self.rect.top > self.alto_ventana:

            self.kill() # Elimina el sprite del enemigo del grupo de sprites si ha salido completamente de la parte inferior de la ventana del juego. El método kill() elimina el sprite de todos los grupos a los que pertenece, lo que permite liberar recursos y mantener el juego eficiente al no procesar enemigos que ya no son visibles en la pantalla.
