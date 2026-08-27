# Requerimientos — Just Climb

## Requerimientos Funcionales

- RF-01: El jugador comienza cada partida en el piso 0.
- RF-02: El jugador puede moverse hacia la izquierda utilizando la flecha izquierda del teclado.
- RF-03: El jugador puede moverse hacia la derecha utilizando la flecha derecha del teclado.
- RF-04: El jugador puede saltar utilizando la barra espaciadora.
- RF-05: El escenario contiene plataformas que permiten al jugador avanzar hacia pisos superiores.
- RF-06: La cámara o el escenario avanza verticalmente cuando el jugador sube.
- RF-07: Aparecen monstruos en diferentes zonas del escenario.
- RF-08: Aparecen objetos peligrosos que el jugador debe esquivar.
- RF-09: El jugador puede recolectar frascos distribuidos por el escenario.
- RF-10: Cada frasco recolectado aumenta el puntaje del jugador.
- RF-11: El jugador comienza cada partida con 3 vidas.
- RF-12: El jugador pierde una vida cuando toca un monstruo u objeto peligroso.
- RF-13: El jugador pierde la partida si sus vidas llegan a 0.
- RF-14: El jugador pierde la partida si cae fuera del escenario.
- RF-15: Aparecen power-ups que pueden ser recolectados por el jugador.
- RF-16: Los power-ups otorgan ventajas temporales al jugador.
- RF-17: La dificultad aumenta a medida que el jugador alcanza pisos superiores.
- RF-18: El juego muestra durante la partida el puntaje, las vidas y el piso alcanzado.
- RF-19: Cuando el jugador pierde, se muestra una pantalla de Game Over.
- RF-20: Al finalizar la partida, el puntaje obtenido se guarda en una base de datos SQLite.
- RF-21: El juego posee una pantalla de ranking con los 5 mejores puntajes.
- RF-22: El jugador puede volver a jugar después de terminar una partida.
- RF-23: El jugador puede salir del juego desde la pantalla final.
- RF-24: El juego posee una pantalla de inicio con el título y una indicación para comenzar.

## Requerimientos No Funcionales

- RNF-01: El juego debe ejecutarse de forma fluida a aproximadamente 60 FPS.
- RNF-02: Los controles deben responder inmediatamente a las teclas presionadas.
- RNF-03: El juego debe desarrollarse en Python utilizando la biblioteca Pygame.
- RNF-04: El ranking debe almacenarse utilizando una base de datos SQLite.
- RNF-05: El código fuente debe estar organizado en módulos separados para facilitar su mantenimiento.
- RNF-06: La ventana del juego debe tener una resolución de 800x600 píxeles.
- RNF-07: La interfaz debe utilizar una estética visual oscura relacionada con el género de horror.
- RNF-08: El proyecto debe mantenerse versionado en GitHub mediante commits descriptivos.
- RNF-09: El juego debe mostrar mensajes claros para indicar las acciones disponibles en cada pantalla.
- RNF-10: Los puntajes deben ordenarse de mayor a menor al mostrar el ranking.
