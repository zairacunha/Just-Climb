import pygame

from camara import Camara # Importa la clase Camara desde el archivo camara.py para poder utilizarla en este script.


ANCHO_VENTANA = 640 # Define el ancho de la ventana del juego en píxeles.

ALTO_VENTANA = 480 # Define el alto de la ventana del juego en píxeles.

ANCHO_MUNDO = 2000 # Define el ancho del mundo del juego en píxeles.

ALTO_MUNDO = 1500 # Define el alto del mundo del juego en píxeles.

TAM_JUGADOR = 40 # Define el tamaño del jugador en píxeles. Se asume que el jugador es un cuadrado de 40x40 píxeles.

VELOCIDAD_JUGADOR = 300 # Define la velocidad del jugador en píxeles por segundo.


def leer_direccion(teclas):

    direccion = pygame.Vector2(0, 0) # Inicializa un vector de dirección en (0, 0) para almacenar la dirección del movimiento del jugador.

    if teclas[pygame.K_LEFT]:

        direccion.x -= 1 # Si la tecla de flecha izquierda está presionada, se decrementa la componente x del vector de dirección en 1, indicando movimiento hacia la izquierda.

    if teclas[pygame.K_RIGHT]:

        direccion.x += 1 # Si la tecla de flecha derecha está presionada, se incrementa la componente x del vector de dirección en 1, indicando movimiento hacia la derecha.

    if teclas[pygame.K_UP]:

        direccion.y -= 1 # Si la tecla de flecha arriba está presionada, se decrementa la componente y del vector de dirección en 1, indicando movimiento hacia arriba.

    if teclas[pygame.K_DOWN]:

        direccion.y += 1 # Si la tecla de flecha abajo está presionada, se incrementa la componente y del vector de dirección en 1, indicando movimiento hacia abajo.

    # Evita que el movimiento diagonal sea más rápido.

    if direccion.length_squared() > 0:

        direccion = direccion.normalize() # Normaliza el vector de dirección para que tenga una longitud de 1, evitando que el movimiento diagonal sea más rápido que el movimiento en línea recta.

    return direccion # Devuelve el vector de dirección resultante, que indica la dirección en la que el jugador debe moverse según las teclas presionadas.


def main():
    pygame.init() # Inicializa todos los módulos de Pygame. Esto es necesario antes de usar cualquier funcionalidad de Pygame.

    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA)) # Crea la ventana del juego con las dimensiones especificadas por ANCHO_VENTANA y ALTO_VENTANA, y asigna la superficie resultante a la variable pantalla.
    pygame.display.set_caption("Ejercicio 1 - Cámara de seguimiento") # Establece el título de la ventana del juego a "Ejercicio 1 - Cámara de seguimiento".

    reloj = pygame.time.Clock()  # Crea un objeto Clock que se utilizará para controlar la velocidad de actualización del juego y medir el tiempo transcurrido entre fotogramas.
    fuente = pygame.font.Font(None, 28) # Crea un objeto Font para renderizar texto en la pantalla. Se utiliza la fuente predeterminada (None) con un tamaño de 28 píxeles.

    limites_mundo = pygame.Rect(0, 0, ANCHO_MUNDO, ALTO_MUNDO) # Define un rectángulo que representa los límites del mundo del juego, comenzando en la posición (0, 0) y con un tamaño de ANCHO_MUNDO x ALTO_MUNDO. Este rectángulo se utilizará para evitar que el jugador salga de los límites del mundo.

    jugador = pygame.Rect(
        ANCHO_MUNDO // 2 - TAM_JUGADOR // 2, # Coloca al jugador en el centro del mundo, ajustando su posición para que esté centrado en relación con su tamaño (TAM_JUGADOR).
        ALTO_MUNDO // 2 - TAM_JUGADOR // 2, # Coloca al jugador en el centro del mundo, ajustando su posición para que esté centrado en relación con su tamaño (TAM_JUGADOR).
        TAM_JUGADOR, # Define el ancho del rectángulo del jugador como TAM_JUGADOR, lo que significa que el jugador será un cuadrado de 40 píxeles de ancho.
        TAM_JUGADOR, # Define el alto del rectángulo del jugador como TAM_JUGADOR, lo que significa que el jugador será un cuadrado de 40 píxeles de alto.
    )
    posicion_jugador = pygame.Vector2(jugador.topleft) # Crea un vector de posición para el jugador basado en la esquina superior izquierda del rectángulo del jugador. Esto se utiliza para almacenar la posición del jugador en coordenadas del mundo y facilitar el movimiento.

    camara = Camara(ANCHO_VENTANA, ALTO_VENTANA) # Crea una instancia de la clase Camara, pasando las dimensiones de la ventana del juego (ANCHO_VENTANA y ALTO_VENTANA) como parámetros. Esta cámara se utilizará para seguir al jugador y ajustar la vista del mundo en función de su posición.

    # Objetos fijos: (rectángulo en coordenadas del mundo, color).
    objetos = [
        (pygame.Rect(200, 180, 120, 80), (220, 80, 70)), # Define un objeto fijo en el mundo del juego representado por un rectángulo en las coordenadas (200, 180) con un tamaño de 120x80 píxeles y un color RGB de (220, 80, 70). Este objeto se dibujará en la pantalla y no se moverá con la cámara.
        (pygame.Rect(700, 400, 100, 140), (80, 190, 120)), # Define otro objeto fijo en el mundo del juego representado por un rectángulo en las coordenadas (700, 400) con un tamaño de 100x140 píxeles y un color RGB de (80, 190, 120). Este objeto también se dibujará en la pantalla y no se moverá con la cámara.
        (pygame.Rect(1200, 250, 180, 90), (230, 190, 60)), # Define otro objeto fijo en el mundo del juego representado por un rectángulo en las coordenadas (1200, 250) con un tamaño de 180x90 píxeles y un color RGB de (230, 190, 60). Este objeto también se dibujará en la pantalla y no se moverá con la cámara.
        (pygame.Rect(1600, 1000, 130, 130), (140, 100, 220)), # Define otro objeto fijo en el mundo del juego representado por un rectángulo en las coordenadas (1600, 1000) con un tamaño de 130x130 píxeles y un color RGB de (140, 100, 220). Este objeto también se dibujará en la pantalla y no se moverá con la cámara.
        (pygame.Rect(400, 1100, 160, 100), (70, 170, 210)), # Define otro objeto fijo en el mundo del juego representado por un rectángulo en las coordenadas (400, 1100) con un tamaño de 160x100 píxeles y un color RGB de (70, 170, 210). Este objeto también se dibujará en la pantalla y no se moverá con la cámara.
    ]

    ejecutando = True # Inicializa la variable ejecutando como True, lo que indica que el bucle principal del juego debe continuar ejecutándose hasta que se cierre la ventana o se detenga el juego.

    while ejecutando:
        dt = reloj.tick(60) / 1000 # Calcula el tiempo transcurrido desde el último fotograma en segundos. Se utiliza el método tick(60) del objeto reloj para limitar la velocidad de actualización a 60 fotogramas por segundo y obtener el tiempo en milisegundos. Luego, se divide entre 1000 para convertirlo a segundos.

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False # Si se detecta un evento de cierre de ventana (QUIT), se establece ejecutando como False para salir del bucle principal y finalizar el juego.

        teclas = pygame.key.get_pressed() # Obtiene el estado actual de todas las teclas del teclado. Devuelve una lista de valores booleanos que indican si cada tecla está presionada (True) o no (False). Esta información se utilizará para determinar la dirección del movimiento del jugador.
        direccion = leer_direccion(teclas) # Llama a la función leer_direccion, pasando el estado de las teclas como argumento, para obtener un vector de dirección que indica hacia dónde debe moverse el jugador en función de las teclas presionadas.

        # El jugador se mueve en coordenadas del mundo.
        posicion_jugador += direccion * VELOCIDAD_JUGADOR * dt # Actualiza la posición del jugador en coordenadas del mundo sumando el vector de dirección multiplicado por la velocidad del jugador y el tiempo transcurrido desde el último fotograma (dt). Esto asegura que el movimiento del jugador sea consistente independientemente de la velocidad de fotogramas.
        jugador.topleft = (round(posicion_jugador.x), round(posicion_jugador.y)) # Actualiza la posición del rectángulo del jugador (jugador) estableciendo su esquina superior izquierda (topleft) en las coordenadas redondeadas de la posición del jugador. Esto asegura que el rectángulo del jugador se dibuje en la posición correcta en la pantalla.

        # El jugador no puede salir del mundo.
        jugador.clamp_ip(limites_mundo) # Ajusta el rectángulo del jugador (jugador) para que permanezca dentro de los límites del mundo definidos por limites_mundo. Si el jugador intenta moverse fuera de estos límites, su posición se ajustará automáticamente para mantenerlo dentro del área permitida.
        posicion_jugador = pygame.Vector2(jugador.topleft) # Actualiza la posición del jugador en coordenadas del mundo después de aplicar la restricción de límites. Esto asegura que la posición del jugador refleje correctamente su ubicación dentro del mundo después de cualquier ajuste realizado por clamp_ip.

        # En este ejercicio no se limita el offset: el jugador queda centrado.
        camara.seguir(jugador) # Llama al método seguir de la instancia de la clase Camara, pasando el rectángulo del jugador (jugador) como argumento. Esto ajusta la posición de la cámara para que siga al jugador, manteniéndolo centrado en la pantalla mientras se mueve por el mundo.

        pantalla.fill((30, 35, 45)) # Rellena la superficie de la pantalla con un color de fondo específico (RGB: 30, 35, 45). Esto borra cualquier contenido anterior en la pantalla antes de dibujar los nuevos elementos del juego.

        for rectangulo, color in objetos:
            pygame.draw.rect(pantalla, color, camara.aplicar(rectangulo)) # Itera sobre la lista de objetos fijos en el mundo del juego. Para cada objeto, se dibuja un rectángulo en la pantalla utilizando pygame.draw.rect. La posición del rectángulo se ajusta mediante el método aplicar de la cámara, que transforma las coordenadas del mundo a las coordenadas de la pantalla, teniendo en cuenta la posición actual de la cámara.

        pygame.draw.rect(
            pantalla, # Dibuja el rectángulo que representa al jugador en la pantalla.
            (40, 180, 255), # Color del jugador en formato RGB (40, 180, 255), que es un tono de azul.
            camara.aplicar(jugador), # Aplica la transformación de la cámara al rectángulo del jugador para obtener su posición en la pantalla, teniendo en cuenta el desplazamiento de la cámara. Esto asegura que el jugador se dibuje correctamente en relación con la vista actual del mundo.
        ) # Dibuja el rectángulo del jugador en la pantalla utilizando el color especificado y la posición ajustada por la cámara.

        texto = fuente.render(
            f"Posición en el mundo: {jugador.x}, {jugador.y}", # Renderiza un texto que muestra la posición actual del jugador en el mundo del juego. Se utiliza el objeto fuente para crear una superficie de texto con el contenido formateado que incluye las coordenadas x e y del rectángulo del jugador (jugador.x, jugador.y).
            True, # Indica que el texto debe renderizarse con antialiasing, lo que suaviza los bordes del texto para que se vea más nítido y menos pixelado.
            (255, 255, 255), # Color del texto en formato RGB (255, 255, 255), que es blanco. Esto asegura que el texto sea claramente visible sobre el fondo oscuro de la pantalla.
        ) # Renderiza el texto que muestra la posición del jugador en el mundo del juego, utilizando la fuente especificada, con antialiasing activado y en color blanco. Esto crea una superficie de texto que se puede dibujar en la pantalla.

        pantalla.blit(texto, (10, 10)) # Dibuja la superficie de texto renderizada en la pantalla en la posición (10, 10) desde la esquina superior izquierda de la ventana. Esto coloca el texto que muestra la posición del jugador en el mundo en la parte superior izquierda de la pantalla.

        pygame.display.flip() # Actualiza la pantalla completa para mostrar todos los elementos dibujados en la superficie de la pantalla. Esto hace que los cambios realizados en la superficie de la pantalla sean visibles para el jugador, mostrando el estado actual del juego en cada fotograma.

    pygame.quit() # Finaliza Pygame y libera todos los recursos utilizados por la biblioteca. Esto se llama al salir del bucle principal del juego para cerrar correctamente la ventana y limpiar los recursos utilizados por Pygame.


if __name__ == "__main__":
    main() # Llama a la función main() para iniciar el juego si este script se ejecuta directamente. Esto asegura que el juego comience solo cuando se ejecute este archivo como programa principal y no cuando se importe como módulo en otro script.
