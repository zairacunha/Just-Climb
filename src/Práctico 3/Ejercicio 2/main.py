
import pygame

from enemigo import Enemigo # Importa la clase Enemigo desde el archivo enemigo.py para poder crear instancias de enemigos en el juego.

from jugador import Jugador # Importa la clase Jugador desde el archivo jugador.py para poder crear una instancia del jugador en el juego.


ANCHO = 800 # Define el ancho de la ventana del juego en píxeles.

ALTO = 600 # Define el alto de la ventana del juego en píxeles.

FPS_OBJETIVO = 60 # Define el número de fotogramas por segundo objetivo para el juego.


def main():

    pygame.init() # Inicializa todos los módulos de Pygame, preparando el entorno para crear la ventana del juego y manejar eventos, gráficos y sonido.

    pantalla = pygame.display.set_mode((ANCHO, ALTO)) # Crea la ventana del juego con las dimensiones especificadas por las constantes ANCHO y ALTO, y devuelve un objeto de superficie (pantalla) que se utilizará para dibujar los elementos del juego.

    pygame.display.set_caption("Ejercicio 2 - Esquivar enemigos") # Establece el título de la ventana del juego a "Ejercicio 2 - Esquivar enemigos", que se mostrará en la barra de título de la ventana.

    reloj = pygame.time.Clock() # Crea un objeto Clock que se utilizará para controlar la velocidad de actualización del juego y medir el tiempo transcurrido entre fotogramas, lo que permite mantener una velocidad de fotogramas constante y sincronizar el movimiento de los elementos del juego.

    fuente = pygame.font.Font(None, 28) # Crea una fuente de texto predeterminada con un tamaño de 28 píxeles, que se utilizará para mostrar información en la pantalla, como el puntaje y los FPS.

    jugador = Jugador(ANCHO, ALTO) # Crea una instancia de la clase Jugador, pasando las dimensiones de la ventana del juego (ANCHO y ALTO) como parámetros para inicializar correctamente la posición y los límites del jugador en el espacio del juego.
    
    todos_los_sprites = pygame.sprite.Group(jugador) # Crea un grupo de sprites que contiene al jugador, lo que permite manejar y actualizar todos los sprites del juego de manera eficiente y organizada, facilitando la detección de colisiones y el dibujo en la pantalla.
    
    enemigos = pygame.sprite.Group() # Crea un grupo de sprites vacío que se utilizará para almacenar todos los enemigos generados durante el juego, lo que permite manejar y actualizar los enemigos de manera eficiente y organizada, facilitando la detección de colisiones y el dibujo en la pantalla.

    timer_enemigo = 0 # Inicializa un temporizador (timer_enemigo) en cero, que se utilizará para controlar la frecuencia con la que se generan nuevos enemigos en el juego. Este temporizador se incrementará con el tiempo transcurrido y, cuando alcance un valor determinado (por ejemplo, 1 segundo), se generará un nuevo enemigo y se reiniciará el temporizador.

    tiempo_sobrevivido = 0 # Inicializa una variable (tiempo_sobrevivido) en cero, que se utilizará para llevar un registro del tiempo total que el jugador ha sobrevivido en el juego. Esta variable se incrementará con el tiempo transcurrido durante la ejecución del juego y se utilizará para calcular el puntaje del jugador, que se mostrará en la pantalla.

    ejecutando = True # Define una variable booleana (ejecutando) que se utilizará como condición para mantener el bucle principal del juego en ejecución hasta que el jugador decida salir del juego o pierda.

    while ejecutando:

        dt = reloj.tick(FPS_OBJETIVO) / 1000 # Calcula el tiempo transcurrido desde el último fotograma en segundos (dt), utilizando el método tick del objeto Clock para limitar la velocidad de actualización del juego a la velocidad de fotogramas objetivo (FPS_OBJETIVO). Esto permite que el movimiento del jugador y otros elementos del juego se realice de manera consistente, independientemente de la velocidad de procesamiento del sistema.

        tiempo_sobrevivido += dt # Incrementa la variable tiempo_sobrevivido con el tiempo transcurrido desde el último fotograma (dt), lo que permite llevar un registro del tiempo total que el jugador ha sobrevivido en el juego. Esta información se utilizará para calcular el puntaje del jugador y mostrarlo en la pantalla.

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                ejecutando = False # Si se detecta un evento de cierre de ventana (QUIT), se establece la variable ejecutando en False, lo que provoca que el bucle principal del juego termine y se cierre la aplicación.

        teclas = pygame.key.get_pressed() # Obtiene el estado actual de todas las teclas del teclado, devolviendo una lista de valores booleanos que indican si cada tecla está presionada o no. Esta información se utilizará para determinar la dirección en la que se moverá el jugador en función de las teclas presionadas.

        # Crea un enemigo cada segundo.

        timer_enemigo += dt # Incrementa el temporizador (timer_enemigo) con el tiempo transcurrido desde el último fotograma (dt), lo que permite llevar un registro del tiempo total transcurrido desde la última vez que se generó un enemigo. Cuando este temporizador alcance o supere 1 segundo, se generará un nuevo enemigo y se reiniciará el temporizador.

        if timer_enemigo >= 1.0:

            timer_enemigo -= 1.0 # Reinicia el temporizador (timer_enemigo) restando 1.0 segundo, lo que permite que el temporizador comience a contar nuevamente desde cero para generar el siguiente enemigo después de otro segundo transcurrido. Esto asegura que los enemigos se generen a intervalos regulares de tiempo durante el juego.

            nuevo_enemigo = Enemigo(ANCHO, ALTO) # Crea una nueva instancia de la clase Enemigo, pasando las dimensiones de la ventana del juego (ANCHO y ALTO) como parámetros para inicializar correctamente la posición y los límites del enemigo en el espacio del juego. Esta instancia representa un nuevo enemigo que aparecerá en la pantalla y se moverá hacia abajo, desafiando al jugador a esquivarlo.

            todos_los_sprites.add(nuevo_enemigo) # Agrega el nuevo enemigo al grupo de sprites (todos_los_sprites), lo que permite que el enemigo se actualice y se dibuje en la pantalla junto con los demás sprites del juego, incluyendo al jugador. Esto facilita la gestión de todos los elementos del juego de manera eficiente y organizada.

            enemigos.add(nuevo_enemigo) # Agrega el nuevo enemigo al grupo de enemigos (enemigos), lo que permite manejar y actualizar específicamente los enemigos del juego de manera eficiente y organizada, facilitando la detección de colisiones con el jugador y el dibujo en la pantalla. Esto asegura que los enemigos se comporten correctamente dentro del juego y puedan interactuar con el jugador según las reglas establecidas.

        todos_los_sprites.update(dt, teclas) # Llama al método update de todos los sprites en el grupo (todos_los_sprites), pasando el tiempo transcurrido desde el último fotograma (dt) y el estado de las teclas presionadas (teclas) como parámetros. Esto permite que cada sprite, incluyendo al jugador y a los enemigos, actualice su posición y comportamiento en función del tiempo y la entrada del usuario, asegurando un movimiento fluido y consistente durante el juego.

        # Comprueba si algún enemigo tocó al jugador.

        if pygame.sprite.spritecollide(jugador, enemigos, False):

            print("¡Game Over!") # Imprime el mensaje "¡Game Over!" en la consola para indicar que el jugador ha sido alcanzado por un enemigo y ha perdido el juego. Esto proporciona retroalimentación al jugador sobre el resultado de la partida y marca el final del juego.

            ejecutando = False # Establece la variable ejecutando en False, lo que provoca que el bucle principal del juego termine y se cierre la aplicación después de que el jugador haya sido alcanzado por un enemigo. Esto asegura que el juego finalice correctamente y permita al jugador reiniciar o salir del juego según lo desee.

        pantalla.fill((30, 30, 30)) # Rellena la superficie de la ventana del juego (pantalla) con un color gris oscuro (RGB: 30, 30, 30) para limpiar la pantalla antes de dibujar los elementos del juego en el siguiente fotograma. Esto asegura que no queden restos de los fotogramas anteriores y proporciona un fondo uniforme para el juego.

        todos_los_sprites.draw(pantalla) # Dibuja todos los sprites en el grupo (todos_los_sprites), incluyendo al jugador y a los enemigos, en la superficie de la ventana del juego (pantalla), utilizando sus posiciones y rectángulos delimitadores para colocarlos correctamente en la pantalla. Esto permite que todos los elementos del juego se muestren visualmente al jugador durante la ejecución del juego.

        puntaje = int(tiempo_sobrevivido * 10) # Calcula el puntaje del jugador multiplicando el tiempo total sobrevivido (tiempo_sobrevivido) por 10 y convirtiéndolo a un número entero. Esto proporciona una forma de medir el rendimiento del jugador en función de cuánto tiempo ha logrado esquivar a los enemigos, y se utilizará para mostrar el puntaje en la pantalla durante el juego.

        texto_puntaje = fuente.render(
            
            f"Puntaje: {puntaje}", True, (255, 255, 255) # Renderiza el texto que muestra el puntaje actual del jugador en la ventana del juego, utilizando la fuente creada anteriormente. El método render toma tres parámetros: el texto a mostrar (f"Puntaje: {puntaje}"), un valor booleano que indica si se debe aplicar antialiasing (True), y el color del texto en formato RGB (255, 255, 255) para que sea blanco. El resultado es una superficie de texto que se puede dibujar en la pantalla.
        )
        texto_fps = fuente.render(
            
            f"FPS: {reloj.get_fps():.0f}", True, (255, 255, 255) # Renderiza el texto que muestra la velocidad de fotogramas actual (FPS) en la ventana del juego, utilizando la fuente creada anteriormente. El método render toma tres parámetros: el texto a mostrar (f"FPS: {reloj.get_fps():.0f}"), un valor booleano que indica si se debe aplicar antialiasing (True), y el color del texto en formato RGB (255, 255, 255) para que sea blanco. El resultado es una superficie de texto que se puede dibujar en la pantalla.
        )

        pantalla.blit(texto_fps, (10, 10)) # Dibuja la superficie de texto que muestra la velocidad de fotogramas (FPS) en la ventana del juego (pantalla) en la posición (10, 10), lo que coloca el texto en la esquina superior izquierda de la ventana para que el jugador pueda ver fácilmente la información de rendimiento del juego.

        pantalla.blit(texto_puntaje, (10, 40)) # Dibuja la superficie de texto que muestra el puntaje actual del jugador en la ventana del juego (pantalla) en la posición (10, 40), lo que coloca el texto justo debajo del texto de FPS en la esquina superior izquierda de la ventana para que el jugador pueda ver fácilmente su puntaje mientras juega.

        pygame.display.flip() # Actualiza la pantalla del juego mostrando todo lo que se ha dibujado en la superficie de la ventana (pantalla) desde el último fotograma. El método flip intercambia los buffers de la pantalla, lo que permite que los cambios realizados en la superficie se reflejen en la ventana del juego de manera eficiente y sin parpadeos.

    pygame.quit() # Cierra todos los módulos de Pygame y libera los recursos utilizados por la biblioteca, finalizando correctamente la aplicación del juego cuando el bucle principal termina y el jugador decide salir del juego. Esto asegura que el programa se cierre de manera ordenada y no deje procesos en ejecución en segundo plano.


if __name__ == "__main__":

    main() # Llama a la función main() para iniciar la ejecución del juego cuando se ejecuta el archivo main.py directamente. Esto permite que el juego se inicie correctamente y se ejecute en un bucle hasta que el jugador decida salir.
