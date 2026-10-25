
class Camara:

    def __init__(self, ancho_ventana, alto_ventana):

        self.ancho_ventana = ancho_ventana # Almacena el ancho de la ventana del juego en la variable de instancia ancho_ventana.

        self.alto_ventana = alto_ventana # Almacena el alto de la ventana del juego en la variable de instancia alto_ventana.

        self.offset_x = 0 # Inicializa el desplazamiento horizontal de la cámara en 0.

        self.offset_y = 0 # Inicializa el desplazamiento vertical de la cámara en 0.

        def seguir(self, jugador, ancho_mundo=None, alto_mundo=None):

            # Calcula el offset para centrar al jugador.

            self.offset_x = jugador.centerx - self.ancho_ventana // 2 # Calcula el desplazamiento horizontal de la cámara para centrar al jugador en la ventana del juego.

            self.offset_y = jugador.centery - self.alto_ventana // 2 # Calcula el desplazamiento vertical de la cámara para centrar al jugador en la ventana del juego.

            # Si se pasan las dimensiones del mundo, limita la cámara para que no muestre espacio fuera de sus bordes.

            if ancho_mundo is not None:

                self.offset_x = max(

                    0,

                    min(self.offset_x, ancho_mundo - self.ancho_ventana) # Limita el desplazamiento horizontal de la cámara para que no muestre espacio fuera del borde derecho del mundo.
                )

            if alto_mundo is not None:

                self.offset_y = max(

                    0,

                    min(self.offset_y, alto_mundo - self.alto_ventana) # Limita el desplazamiento vertical de la cámara para que no muestre espacio fuera del borde inferior del mundo.
                )

        def aplicar(self, rectangulo):

            # Devuelve el rectángulo trasladado a coordenadas de pantalla.

            return rectangulo.move(

                -self.offset_x, - self.offset_y # Aplica el desplazamiento de la cámara al rectángulo para obtener sus coordenadas en la pantalla del juego.
            )
