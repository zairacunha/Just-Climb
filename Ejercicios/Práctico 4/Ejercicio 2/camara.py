
class Camara:
    def __init__(self, ancho_ventana, alto_ventana):
        # Guarda las dimensiones de la ventana del juego.
        self.ancho_ventana = ancho_ventana
        self.alto_ventana = alto_ventana

        # El offset indica cuánto se desplazó la cámara desde el origen.
        self.offset_x = 0
        self.offset_y = 0

    def seguir(self, jugador, ancho_mundo=None, alto_mundo=None):
        # Calcula el desplazamiento para centrar al jugador en la ventana.
        self.offset_x = jugador.centerx - self.ancho_ventana // 2
        self.offset_y = jugador.centery - self.alto_ventana // 2

        # Si se indicó el ancho del mundo, evita que la cámara
        # sobrepase sus bordes izquierdo y derecho.
        if ancho_mundo is not None:
            max_offset_x = max(0, ancho_mundo - self.ancho_ventana)
            self.offset_x = max(0, min(self.offset_x, max_offset_x))

        # Si se indicó el alto del mundo, evita que la cámara
        # sobrepase sus bordes superior e inferior.
        if alto_mundo is not None:
            max_offset_y = max(0, alto_mundo - self.alto_ventana)
            self.offset_y = max(0, min(self.offset_y, max_offset_y))

    def aplicar(self, rectangulo):
        # Convierte un rectángulo de coordenadas del mundo
        # a coordenadas visibles en la ventana.
        return rectangulo.move(-self.offset_x, -self.offset_y)
