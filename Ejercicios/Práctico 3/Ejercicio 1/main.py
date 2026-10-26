
import pygame

from jugador import Jugador # Importa la clase Jugador desde el archivo jugador.py para poder crear una instancia del jugador en el juego.


ANCHO = 800 # Define el ancho de la ventana del juego en píxeles.

ALTO = 600 # Define el alto de la ventana del juego en píxeles.

FPS_OBJETIVO = 60 # Define la velocidad de fotogramas objetivo del juego en cuadros por segundo.


def main():

    pygame.init() # Inicializa todos los módulos de Pygame, preparando el entorno para crear la ventana del juego y manejar eventos, gráficos y sonido.

    pantalla = pygame.display.set_mode((ANCHO, ALTO)) # Crea la ventana del juego con las dimensiones especificadas por las constantes ANCHO y ALTO, y devuelve un objeto de superficie (pantalla) que se utilizará para dibujar los elementos del juego.

    pygame.display.set_caption("Ejercicio 1 - Jugador Sprite") # Establece el título de la ventana del juego a "Ejercicio 1 - Jugador Sprite", que se mostrará en la barra de título de la ventana.

    reloj = pygame.time.Clock() # Crea un objeto Clock que se utilizará para controlar la velocidad de actualización del juego y medir el tiempo transcurrido entre fotogramas, lo que permite mantener una velocidad de fotogramas constante y sincronizar el movimiento de los elementos del juego.

    fuente = pygame.font.Font(None, 28) # Crea una fuente de texto predeterminada con un tamaño de 28 píxeles.

    jugador = Jugador(ANCHO, ALTO) # Crea una instancia de la clase Jugador, pasando las dimensiones de la ventana del juego (ANCHO y ALTO) como parámetros para inicializar correctamente la posición y los límites del jugador en el espacio del juego.

    sprites = pygame.sprite.Group(jugador) # Crea un grupo de sprites que contiene al jugador, lo que permite manejar y actualizar todos los sprites del juego de manera eficiente y organizada, facilitando la detección de colisiones y el dibujo en la pantalla.

    ejecutando = True # Define una variable booleana (ejecutando) que se utilizará como condición para mantener el bucle principal del juego en ejecución hasta que el jugador decida salir del juego.

    while ejecutando:

        dt = reloj.tick(FPS_OBJETIVO) / 1000 # Calcula el tiempo transcurrido desde el último fotograma en segundos (dt), utilizando el método tick del objeto Clock para limitar la velocidad de actualización del juego a la velocidad de fotogramas objetivo (FPS_OBJETIVO). Esto permite que el movimiento del jugador y otros elementos del juego se realice de manera consistente, independientemente de la velocidad de procesamiento del sistema.

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                ejecutando = False # Si se detecta un evento de cierre de ventana (QUIT), se establece la variable ejecutando en False, lo que provoca que el bucle principal del juego termine y se cierre la aplicación.

        teclas = pygame.key.get_pressed() # Obtiene el estado actual de todas las teclas del teclado, devolviendo una lista de valores booleanos que indican si cada tecla está presionada o no. Esta información se utilizará para determinar la dirección en la que se moverá el jugador en función de las teclas presionadas.

        sprites.update(dt, teclas) # Llama al método update de todos los sprites en el grupo (en este caso, solo el jugador), pasando el tiempo transcurrido desde el último fotograma (dt) y el estado de las teclas presionadas (teclas) como parámetros. Esto permite que cada sprite actualice su posición y comportamiento en función del tiempo y la entrada del usuario.

        pantalla.fill((30, 30, 30)) # Rellena la superficie de la ventana del juego (pantalla) con un color gris oscuro (RGB: 30, 30, 30) para limpiar la pantalla antes de dibujar los elementos del juego en el siguiente fotograma.

        sprites.draw(pantalla) # Dibuja todos los sprites en el grupo (en este caso, solo el jugador) en la superficie de la ventana del juego (pantalla), utilizando sus posiciones y rectángulos delimitadores para colocarlos correctamente en la pantalla.

        texto_fps = fuente.render(
            
            f"FPS: {reloj.get_fps():.0f}", True, (255, 255, 255) # Renderiza el texto que muestra la velocidad de fotogramas actual (FPS) en la ventana del juego, utilizando la fuente creada anteriormente. El método render toma tres parámetros: el texto a mostrar (f"FPS: {reloj.get_fps():.0f}"), un valor booleano que indica si se debe aplicar antialiasing (True), y el color del texto en formato RGB (255, 255, 255) para que sea blanco. El resultado es una superficie de texto que se puede dibujar en la pantalla.
        )
        
        pantalla.blit(texto_fps, (10, 10)) # Dibuja la superficie de texto que muestra la velocidad de fotogramas (FPS) en la ventana del juego (pantalla) en la posición (10, 10), lo que coloca el texto en la esquina superior izquierda de la ventana para que el jugador pueda ver fácilmente la información de rendimiento del juego.

        pygame.display.flip() # Actualiza la pantalla del juego mostrando todo lo que se ha dibujado en la superficie de la ventana (pantalla) desde el último fotograma. El método flip intercambia los buffers de la pantalla, lo que permite que los cambios realizados en la superficie se reflejen en la ventana del juego de manera eficiente y sin parpadeos.

    pygame.quit() # Cierra todos los módulos de Pygame y libera los recursos utilizados por la biblioteca, finalizando correctamente la aplicación del juego cuando el bucle principal termina y el jugador decide salir del juego.


if __name__ == "__main__":

    main() # Llama a la función main() para iniciar la ejecución del juego cuando se ejecuta el archivo main.py directamente. Esto permite que el juego se inicie correctamente y se ejecute en un bucle hasta que el jugador decida salir.
