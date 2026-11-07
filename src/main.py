"""
JUST CLIMB — primer prototipo jugable

Juego 2D de plataformas verticales hecho con Python y Pygame.
Este prototipo utiliza formas geométricas y colores. Los sonidos son opcionales:
si están en assets/sounds, se cargan automáticamente. La cámara sigue el ascenso
del personaje, mientras las plataformas, frascos y power-ups se generan al
iniciar la partida. Los monstruos aparecen de vez en cuando por arriba y caen
hacia el jugador.

Requisitos:
    Python 3.8 o superior
    pygame (instalar con: python -m pip install pygame)

Ejecución recomendada desde la raíz del repositorio:
    python src/main.py

Los valores de física, la meta de altura y la frecuencia de aparición de objetos
son provisionales y se pueden ajustar en la sección de constantes.
"""

# ============================================================================
# 1. IMPORTACIONES
# ============================================================================

import random
import sqlite3
from datetime import datetime
from pathlib import Path

import pygame


# ============================================================================
# 2. CONFIGURACIÓN Y CONSTANTES DEL JUEGO
# ============================================================================

ANCHO = 800
ALTO = 600
FPS = 60

# Colores de la ambientación oscura.
COLOR_FONDO = (18, 20, 31)
COLOR_PANEL = (35, 37, 53)
COLOR_TEXTO = (238, 238, 242)
COLOR_SECUNDARIO = (177, 181, 198)
COLOR_PLATAFORMA = (100, 190, 145)
COLOR_JUGADOR = (245, 190, 90)
COLOR_FRASCO = (90, 205, 230)

# Física y movimiento. Estos números se ajustan probando el juego.
GRAVEDAD = 0.55
FUERZA_SALTO = -13.5
VELOCIDAD_HORIZONTAL = 6

# Las plataformas se mantienen a una distancia alcanzable con un salto normal.
# También se limita cuánto puede desplazarse cada plataforma respecto de la anterior.
SEPARACION_PLATAFORMA_MIN = 68
SEPARACION_PLATAFORMA_MAX = 92
DESPLAZAMIENTO_PLATAFORMA_MAX = 120

# Los enemigos nuevos aparecen con pausas aleatorias y caen desde arriba.
INTERVALO_ENEMIGO_MIN = 1600
INTERVALO_ENEMIGO_MAX = 3200
VELOCIDAD_ENEMIGO_MIN = 4
VELOCIDAD_ENEMIGO_MAX = 6

# Tamaño de los objetos del juego.
ANCHO_JUGADOR = 36
ALTO_JUGADOR = 44
ANCHO_PLATAFORMA = 105
ALTO_PLATAFORMA = 15

# La partida termina con victoria al alcanzar el piso 100.
# Cada piso representa 500 píxeles de ascenso, medidos desde el piso 0.
MAX_PISOS = 100
ALTURA_POR_PISO = 500
ALTURA_META = MAX_PISOS * ALTURA_POR_PISO

# Duraciones de poderes temporales, expresadas en milisegundos.
DURACION_ESCUDO = 10_000
DURACION_SALTO_ALTO = 5 * 60 * 1000
DURACION_TIEMPO_DETENIDO = 3_000

# Detecta la raíz del proyecto tanto si se ejecuta src/main.py como main.py
# desde la carpeta principal del repositorio.
CARPETA_SCRIPT = Path(__file__).resolve().parent
CARPETA_PROYECTO = CARPETA_SCRIPT.parent if CARPETA_SCRIPT.name == "src" else CARPETA_SCRIPT
RUTA_BASE_DATOS = CARPETA_PROYECTO / "database" / "ranking.db"

# Audios que el juego intenta cargar desde la carpeta de recursos.
RUTA_SONIDOS = CARPETA_PROYECTO / "assets" / "sounds"
RUTA_PANEL_HUD = CARPETA_PROYECTO / "assets" / "images" / "ui" / "hud_panel.png"
RUTA_SPRITES = CARPETA_PROYECTO / "assets" / "images" / "kenney_1bit"
RUTA_FUENTE = CARPETA_PROYECTO / "assets" / "fonts" / "Kenney Pixel.ttf"
NOMBRES_AUDIO = {
    # Los nombres que Ronron proporcionó aparecen primero para que se usen
    # exactamente esos archivos cuando estén en assets/sounds/.
    "musica": ("musica", "music", "background_music"),
    "game_over": ("game_over", "gameover"),
    "punto": ("punto", "recoger_punto", "collect_point", "collect"),
    "vida": ("choque", "perder_vida", "vida_perdida", "lose_life", "hit"),
}
EXTENSIONES_MUSICA = (".ogg", ".mp3", ".wav")
EXTENSIONES_EFECTO = (".wav", ".ogg")


def cargar_sonidos():
    """Carga los audios disponibles; el juego sigue funcionando si faltan."""
    sonidos = {"musica": False, "game_over": None, "punto": None, "vida": None}

    # Algunas computadoras o entornos de prueba no tienen dispositivo de audio.
    # En ese caso se desactiva el sonido sin impedir que el juego abra.
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    except pygame.error as error:
        print("Aviso: no se pudo iniciar el audio; el juego continuará sin sonido. {}".format(error))
        return sonidos

    for clave, nombres in NOMBRES_AUDIO.items():
        extensiones = EXTENSIONES_MUSICA if clave == "musica" else EXTENSIONES_EFECTO
        ruta_audio = None

        # Se aceptan algunos nombres comunes para no exigir un nombre único.
        for nombre in nombres:
            for extension in extensiones:
                candidato = RUTA_SONIDOS / (nombre + extension)
                if candidato.is_file():
                    ruta_audio = candidato
                    break
            if ruta_audio:
                break

        if ruta_audio is None:
            print("Aviso: falta el audio '{}'; se omitirá ese sonido.".format(clave))
            continue

        try:
            if clave == "musica":
                pygame.mixer.music.load(str(ruta_audio))
                sonidos[clave] = True
            else:
                sonidos[clave] = pygame.mixer.Sound(str(ruta_audio))
        except pygame.error as error:
            print("Aviso: no se pudo cargar '{}': {}".format(ruta_audio.name, error))

    return sonidos


def cargar_panel_hud():
    """Carga el marco decorativo del HUD si el recurso está disponible."""
    if not RUTA_PANEL_HUD.is_file():
        print("Aviso: no se encontró el panel del HUD; se usará el marco simple.")
        return None

    try:
        # Se usa convert_alpha para mantener la transparencia del PNG de Kenney.
        return pygame.image.load(str(RUTA_PANEL_HUD)).convert_alpha()
    except (pygame.error, OSError) as error:
        print("Aviso: no se pudo cargar el panel del HUD; se usará el marco simple. {}".format(error))
        return None


def cargar_sprites():
    """Carga los sprites elegidos del pack; los que falten usan dibujos simples."""
    nombres = ("player", "enemy", "platform", "powerup")
    sprites = {}

    for nombre in nombres:
        ruta = RUTA_SPRITES / (nombre + ".png")
        try:
            sprites[nombre] = pygame.image.load(str(ruta)).convert_alpha()
        except (pygame.error, OSError) as error:
            sprites[nombre] = None
            print("Aviso: no se pudo cargar el sprite '{}': {}".format(nombre, error))

    return sprites


def cargar_fuentes():
    """Carga la fuente pixelada y usa la tipografía de Pygame como respaldo."""
    tamanos = (64, 30, 24)

    try:
        if RUTA_FUENTE.is_file():
            # Se reutiliza la misma familia tipográfica en títulos, textos y HUD
            # para mantener una apariencia pixelada coherente en todo el juego.
            return tuple(pygame.font.Font(str(RUTA_FUENTE), tamano) for tamano in tamanos)

        print("Aviso: no se encontró Kenney Pixel; se usará la fuente predeterminada.")
    except (pygame.error, OSError) as error:
        print("Aviso: no se pudo cargar Kenney Pixel; se usará la fuente predeterminada. {}".format(error))

    # El juego sigue siendo ejecutable aunque falte o esté dañada la fuente.
    return tuple(pygame.font.Font(None, tamano) for tamano in tamanos)


def iniciar_musica(sonidos):
    """Reproduce la música de fondo en bucle si se pudo cargar."""
    if sonidos.get("musica"):
        try:
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass


def detener_musica():
    """Detiene la música de fondo, por ejemplo al terminar la partida."""
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
    except pygame.error:
        pass


def reproducir_efecto(sonidos, nombre):
    """Reproduce un efecto disponible sin interrumpir el juego si falla."""
    efecto = sonidos.get(nombre) if sonidos else None
    if efecto is not None:
        try:
            efecto.play()
        except pygame.error:
            pass


# ============================================================================
# 3. FUNCIONES DE BASE DE DATOS SQLITE
# ============================================================================

def preparar_base_datos(ruta=None):
    """Crea la carpeta y la tabla del ranking si todavía no existen."""
    ruta = Path(ruta) if ruta else RUTA_BASE_DATOS
    ruta.parent.mkdir(parents=True, exist_ok=True)

    # El bloque with cierra la conexión incluso si ocurre un error.
    with sqlite3.connect(str(ruta)) as conexion:
        conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS ranking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                puntaje INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                piso INTEGER NOT NULL
            )
            """
        )
        conexion.commit()
    return ruta


def guardar_puntaje(nombre, puntaje, piso, ruta=None):
    """Guarda el resultado de una partida en SQLite."""
    ruta = preparar_base_datos(ruta)
    nombre = nombre.strip() or "Jugador"
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    with sqlite3.connect(str(ruta)) as conexion:
        conexion.execute(
            "INSERT INTO ranking (nombre, puntaje, fecha, piso) VALUES (?, ?, ?, ?)",
            (nombre[:20], int(puntaje), int(piso), fecha),
        )
        conexion.commit()


def obtener_mejores_puntajes(ruta=None):
    """Devuelve una lista con los cinco mejores resultados guardados."""
    ruta = preparar_base_datos(ruta)

    with sqlite3.connect(str(ruta)) as conexion:
        filas = conexion.execute(
            """
            SELECT nombre, puntaje, fecha, piso
            FROM ranking
            ORDER BY puntaje DESC, id ASC
            LIMIT 5
            """
        ).fetchall()

    return filas


# ============================================================================
# 4. CREACIÓN DEL ESCENARIO Y DE LOS OBJETOS
# ============================================================================

def crear_escenario():
    """Genera plataformas, frascos y poderes para una partida nueva."""
    plataformas = []
    frascos = []
    poderes = []

    # Plataforma inicial ancha: sirve como punto de partida seguro.
    plataforma_inicial = pygame.Rect(ANCHO // 2 - 90, 520, 180, ALTO_PLATAFORMA)
    plataformas.append(plataforma_inicial)

    # Se crean plataformas hacia arriba. En coordenadas del mundo, subir
    # significa que la coordenada Y se vuelve más pequeña.
    y = plataforma_inicial.y
    plataforma_anterior = plataforma_inicial
    cantidad_plataformas = int(ALTURA_META / SEPARACION_PLATAFORMA_MIN) + 25

    for indice in range(cantidad_plataformas):
        # La distancia vertical es menor que antes para que el salto sea más fácil.
        separacion = random.randint(
            SEPARACION_PLATAFORMA_MIN,
            SEPARACION_PLATAFORMA_MAX,
        )
        y -= separacion

        # En vez de elegir cualquier punto de la pantalla, limitamos el cambio
        # horizontal tomando como referencia la plataforma anterior. Así se
        # evita que aparezca una plataforma demasiado lejos para alcanzarla.
        centro_anterior = plataforma_anterior.centerx
        desplazamiento = random.randint(
            -DESPLAZAMIENTO_PLATAFORMA_MAX,
            DESPLAZAMIENTO_PLATAFORMA_MAX,
        )
        centro_nuevo = max(
            ANCHO_PLATAFORMA // 2 + 10,
            min(ANCHO - ANCHO_PLATAFORMA // 2 - 10,
                centro_anterior + desplazamiento),
        )
        x = centro_nuevo - ANCHO_PLATAFORMA // 2
        plataforma = pygame.Rect(x, y, ANCHO_PLATAFORMA, ALTO_PLATAFORMA)
        plataformas.append(plataforma)
        plataforma_anterior = plataforma

        # Algunas plataformas pueden tener un frasco o un power-up.
        if random.random() < 0.27:
            frasco = pygame.Rect(x + random.randint(8, 70), y - 34, 18, 24)
            frascos.append(frasco)

        # A Second Chance aparece como máximo una vez por partida.
        if indice == 12:
            poderes.append({
                "rect": pygame.Rect(x + 42, y - 42, 30, 30),
                "tipo": "vida",
            })
        elif random.random() < 0.075:
            tipo = random.choice(["escudo", "salto", "tiempo", "teletransporte"])
            poderes.append({
                "rect": pygame.Rect(x + 42, y - 42, 30, 30),
                "tipo": tipo,
            })

    return plataformas, frascos, poderes


def nuevo_estado_partida():
    """Prepara las variables de una partida nueva."""
    jugador = pygame.Rect(ANCHO // 2 - ANCHO_JUGADOR // 2, 462,
                          ANCHO_JUGADOR, ALTO_JUGADOR)
    plataformas, frascos, poderes = crear_escenario()

    return {
        "jugador": jugador,
        "velocidad_y": 0.0,
        "en_plataforma": False,
        "plataformas": plataformas,
        "enemigos_caida": [],
        "proximo_enemigo_ms": (
            pygame.time.get_ticks()
            + random.randint(INTERVALO_ENEMIGO_MIN, INTERVALO_ENEMIGO_MAX)
        ),
        "frascos": frascos,
        "poderes": poderes,
        "camara_y": 0.0,
        "altura_maxima": 0,
        "puntaje": 0,
        "vidas": 3,
        "invulnerable_hasta": 0,
        "escudo_hasta": 0,
        "salto_alto_hasta": 0,
        "tiempo_detenido_hasta": 0,
        "puede_controlar_tiempo": False,
        "puede_teletransportarse": False,
        "tiempo_ya_usado": False,
        "teletransporte_ya_usado": False,
        "motivo_fin": "",
        "victoria": False,
    }


# ============================================================================
# 5. FUNCIONES DE DIBUJO E INTERFAZ
# ============================================================================

def dibujar_texto(pantalla, fuente, texto, x, y, color=COLOR_TEXTO, centrado=False):
    """Dibuja texto en pantalla, con opción de centrarlo horizontalmente."""
    superficie = fuente.render(str(texto), True, color)
    if centrado:
        x -= superficie.get_width() // 2
    pantalla.blit(superficie, (x, y))
    return superficie.get_rect(topleft=(x, y))


def dibujar_sprite(pantalla, sprites, nombre, rectangulo, tinte=None):
    """Dibuja un sprite escalado sin suavizado para conservar el pixel art."""
    imagen = sprites.get(nombre) if sprites else None
    if imagen is None:
        return False

    # Se escala con transform.scale, no smoothscale, para mantener bordes nítidos.
    imagen = imagen.copy()
    if tinte:
        imagen.fill((*tinte, 255), special_flags=pygame.BLEND_RGBA_MULT)

    # Se conserva la proporción original y se centra dentro de la caja lógica.
    factor = min(
        rectangulo.width / imagen.get_width(),
        rectangulo.height / imagen.get_height(),
    )
    ancho = max(1, int(imagen.get_width() * factor))
    alto = max(1, int(imagen.get_height() * factor))
    imagen = pygame.transform.scale(imagen, (ancho, alto))
    destino = imagen.get_rect(center=rectangulo.center)
    pantalla.blit(imagen, destino.topleft)
    return True


def dibujar_plataforma_texturizada(pantalla, rectangulo, sprites):
    """Repite el tile de plataforma horizontalmente, sin estirar sus píxeles."""
    imagen = sprites.get("platform") if sprites else None
    if imagen is None:
        return False

    # El tile original es de 16x16; solo se adapta su alto al collider actual.
    tile = pygame.transform.scale(imagen, (16, rectangulo.height)).copy()
    tile.fill((190, 235, 205, 255), special_flags=pygame.BLEND_RGBA_MULT)

    for x in range(rectangulo.left, rectangulo.right, tile.get_width()):
        ancho_visible = min(tile.get_width(), rectangulo.right - x)
        segmento = tile.subsurface(pygame.Rect(0, 0, ancho_visible, tile.get_height()))
        pantalla.blit(segmento, (x, rectangulo.top))
    return True


def dibujar_boton(pantalla, fuente, rectangulo, texto, seleccionado=False):
    """Dibuja un botón simple que se puede usar con mouse o teclado."""
    color = (100, 74, 92) if seleccionado else COLOR_PANEL
    pygame.draw.rect(pantalla, color, rectangulo, border_radius=9)
    pygame.draw.rect(pantalla, (130, 134, 155), rectangulo, 2, border_radius=9)
    dibujar_texto(
        pantalla, fuente, texto,
        rectangulo.centerx, rectangulo.centery - fuente.get_height() // 2,
        COLOR_TEXTO, centrado=True,
    )


def dibujar_panel_hud(pantalla, rectangulo, textura):
    """Dibuja un panel con marco de Kenney sin estirar ni deformar sus esquinas."""
    # La base oscura mantiene el texto legible sobre cualquier parte del escenario.
    fondo = pygame.Surface(rectangulo.size, pygame.SRCALPHA)
    fondo.fill((12, 14, 24, 225))
    pantalla.blit(fondo, rectangulo.topleft)

    # Si el PNG falta, usamos un marco sencillo para que el HUD siga funcionando.
    if textura is None:
        pygame.draw.rect(pantalla, (70, 74, 92), rectangulo, 2, border_radius=8)
        return

    # El PNG elegido mide 48x48. Se divide en nueve partes para conservar las
    # esquinas y escalar únicamente los bordes y el centro al tamaño del HUD.
    tamano_esquina = 12
    ancho_textura, alto_textura = textura.get_size()
    tamano_esquina = min(tamano_esquina, ancho_textura // 3, alto_textura // 3)

    ancho_centro = ancho_textura - tamano_esquina * 2
    alto_centro = alto_textura - tamano_esquina * 2
    ancho_destino_centro = max(1, rectangulo.width - tamano_esquina * 2)
    alto_destino_centro = max(1, rectangulo.height - tamano_esquina * 2)

    # Cada par indica la zona de origen y su posición/tamaño de destino.
    partes = [
        ((0, 0, tamano_esquina, tamano_esquina),
         (rectangulo.left, rectangulo.top, tamano_esquina, tamano_esquina)),
        ((tamano_esquina, 0, ancho_centro, tamano_esquina),
         (rectangulo.left + tamano_esquina, rectangulo.top,
          ancho_destino_centro, tamano_esquina)),
        ((ancho_textura - tamano_esquina, 0, tamano_esquina, tamano_esquina),
         (rectangulo.right - tamano_esquina, rectangulo.top,
          tamano_esquina, tamano_esquina)),
        ((0, tamano_esquina, tamano_esquina, alto_centro),
         (rectangulo.left, rectangulo.top + tamano_esquina,
          tamano_esquina, alto_destino_centro)),
        ((tamano_esquina, tamano_esquina, ancho_centro, alto_centro),
         (rectangulo.left + tamano_esquina, rectangulo.top + tamano_esquina,
          ancho_destino_centro, alto_destino_centro)),
        ((ancho_textura - tamano_esquina, tamano_esquina,
          tamano_esquina, alto_centro),
         (rectangulo.right - tamano_esquina, rectangulo.top + tamano_esquina,
          tamano_esquina, alto_destino_centro)),
        ((0, alto_textura - tamano_esquina, tamano_esquina, tamano_esquina),
         (rectangulo.left, rectangulo.bottom - tamano_esquina,
          tamano_esquina, tamano_esquina)),
        ((tamano_esquina, alto_textura - tamano_esquina,
          ancho_centro, tamano_esquina),
         (rectangulo.left + tamano_esquina, rectangulo.bottom - tamano_esquina,
          ancho_destino_centro, tamano_esquina)),
        ((ancho_textura - tamano_esquina, alto_textura - tamano_esquina,
          tamano_esquina, tamano_esquina),
         (rectangulo.right - tamano_esquina, rectangulo.bottom - tamano_esquina,
          tamano_esquina, tamano_esquina)),
    ]

    for origen, destino in partes:
        recorte = textura.subsurface(pygame.Rect(origen)).copy()
        # El PNG original es blanco; se tiñe a borgoña para armonizar con el horror.
        recorte.fill((190, 120, 145, 255), special_flags=pygame.BLEND_RGBA_MULT)
        recorte = pygame.transform.scale(recorte, (destino[2], destino[3]))
        # Un toque de transparencia suaviza el blanco del marco para la estética oscura.
        recorte.set_alpha(210)
        pantalla.blit(recorte, (destino[0], destino[1]))


def dibujar_fondo(pantalla):
    """Pinta el fondo y unas líneas tenues para dar sensación de edificio."""
    pantalla.fill(COLOR_FONDO)
    for x in range(40, ANCHO, 120):
        pygame.draw.line(pantalla, (27, 30, 43), (x, 0), (x, ALTO), 1)
    for y in range(35, ALTO, 100):
        pygame.draw.line(pantalla, (25, 28, 40), (0, y), (ANCHO, y), 1)


def dibujar_menu(pantalla, fuentes, seleccion):
    """Muestra el menú principal."""
    dibujar_fondo(pantalla)
    fuente_titulo, fuente, _ = fuentes
    dibujar_texto(pantalla, fuente_titulo, "JUST CLIMB", ANCHO // 2, 115,
                  (220, 90, 105), centrado=True)
    dibujar_texto(pantalla, fuente, "Escapa del edificio abandonado",
                  ANCHO // 2, 185, COLOR_SECUNDARIO, centrado=True)

    opciones = ["ESCAPE - Jugar", "HELP - Ayuda", "GIVE UP - Salir"]
    botones = []
    for indice, opcion in enumerate(opciones):
        rectangulo = pygame.Rect(ANCHO // 2 - 150, 275 + indice * 68, 300, 50)
        dibujar_boton(pantalla, fuente, rectangulo, opcion, indice == seleccion)
        botones.append(rectangulo)

    dibujar_texto(pantalla, fuente, "Flechas para elegir · Enter para confirmar",
                  ANCHO // 2, 510, COLOR_SECUNDARIO, centrado=True)
    return botones


def dibujar_ayuda(pantalla, fuentes):
    """Muestra los controles y explica brevemente las reglas."""
    dibujar_fondo(pantalla)
    fuente_titulo, fuente, fuente_pequena = fuentes
    dibujar_texto(pantalla, fuente_titulo, "AYUDA", ANCHO // 2, 55,
                  (220, 90, 105), centrado=True)

    lineas = [
        "Flecha izquierda / derecha: moverte por el escenario.",
        "Barra espaciadora: saltar cuando estás sobre una plataforma.",
        "R: activar Control del tiempo si ya lo recogiste.",
        "T: usar Teletransporte si ya lo recogiste.",
        "",
        "Aterriza sobre plataformas y asciende hasta la meta.",
        "Esquiva las criaturas; cada golpe resta una vida.",
        "Recoge frascos para sumar puntos.",
        "Escudo: 10 segundos. Super Bunny Jump: 5 minutos.",
        "A Second Chance: suma una vida. La caída termina la partida.",
        "Control del tiempo y Teletransporte se usan una vez.",
        "",
        "Pulsa ESC o ENTER para volver al menú.",
    ]
    for indice, linea in enumerate(lineas):
        dibujar_texto(pantalla, fuente_pequena, linea, ANCHO // 2, 145 + indice * 30,
                      COLOR_TEXTO, centrado=True)


def dibujar_partida(pantalla, fuentes, estado, ahora, textura_hud=None, sprites=None):
    """Dibuja el escenario, el personaje y el HUD."""
    dibujar_fondo(pantalla)
    fuente_titulo, fuente, fuente_pequena = fuentes
    camara_y = estado["camara_y"]

    # Solo dibujamos objetos cercanos a la pantalla para evitar trabajo inútil.
    for plataforma in estado["plataformas"]:
        y_pantalla = plataforma.y - camara_y
        if -40 <= y_pantalla <= ALTO + 40:
            rect = pygame.Rect(plataforma.x, int(y_pantalla), plataforma.w, plataforma.h)
            if not dibujar_plataforma_texturizada(pantalla, rect, sprites):
                pygame.draw.rect(pantalla, COLOR_PLATAFORMA, rect, border_radius=5)
                pygame.draw.rect(pantalla, (44, 98, 78), rect, 2, border_radius=5)

    for frasco in estado["frascos"]:
        y_pantalla = frasco.y - camara_y
        if -40 <= y_pantalla <= ALTO + 40:
            rect = pygame.Rect(frasco.x, int(y_pantalla), frasco.w, frasco.h)
            # El pack no contiene un frasco inequívoco; conservamos el dibujo
            # provisional para que el objeto siga siendo reconocible.
            pygame.draw.rect(pantalla, COLOR_FRASCO, rect, border_radius=4)
            pygame.draw.rect(pantalla, (200, 250, 255), (rect.x + 5, rect.y + 4, 4, 14))

    # Los monstruos que caen se dibujan como criaturas violetas con ojos rojos.
    # Su posición se guarda en coordenadas del mundo y se convierte a pantalla.
    for enemigo in estado["enemigos_caida"]:
        rect_original = enemigo["rect"]
        y_pantalla = rect_original.y - camara_y
        if -45 <= y_pantalla <= ALTO + 45:
            rect = pygame.Rect(
                rect_original.x,
                int(y_pantalla),
                rect_original.w,
                rect_original.h,
            )
            if not dibujar_sprite(pantalla, sprites, "enemy", rect, (230, 155, 210)):
                pygame.draw.ellipse(pantalla, (150, 75, 175), rect)
                pygame.draw.ellipse(pantalla, (70, 35, 90), rect, 2)
                pygame.draw.circle(pantalla, (245, 80, 100),
                                   (rect.centerx - 6, rect.centery - 3), 3)
                pygame.draw.circle(pantalla, (245, 80, 100),
                                   (rect.centerx + 6, rect.centery - 3), 3)

    colores_poder = {
        "escudo": (90, 155, 240),
        "salto": (190, 110, 230),
        "vida": (230, 75, 105),
        "tiempo": (90, 215, 205),
        "teletransporte": (245, 170, 70),
    }
    letras_poder = {"escudo": "E", "salto": "S", "vida": "+", "tiempo": "R", "teletransporte": "T"}
    for poder in estado["poderes"]:
        rect_original = poder["rect"]
        y_pantalla = rect_original.y - camara_y
        if -40 <= y_pantalla <= ALTO + 40:
            rect = pygame.Rect(rect_original.x, int(y_pantalla), rect_original.w, rect_original.h)
            if dibujar_sprite(pantalla, sprites, "powerup", rect, colores_poder[poder["tipo"]]):
                dibujar_texto(pantalla, fuente_pequena, letras_poder[poder["tipo"]],
                              rect.centerx, rect.centery - fuente_pequena.get_height() // 2,
                              COLOR_TEXTO, centrado=True)
            else:
                pygame.draw.rect(pantalla, colores_poder[poder["tipo"]], rect, border_radius=8)
                dibujar_texto(pantalla, fuente_pequena, letras_poder[poder["tipo"]],
                              rect.centerx, rect.centery - fuente_pequena.get_height() // 2,
                              COLOR_TEXTO, centrado=True)

    jugador = estado["jugador"]
    jugador_pantalla = pygame.Rect(jugador.x, int(jugador.y - camara_y), jugador.w, jugador.h)
    protegido = ahora < estado["escudo_hasta"] or ahora < estado["invulnerable_hasta"]

    # Alternar el parpadeo al recibir daño; así se nota la invulnerabilidad.
    mostrar_jugador = not (protegido and (ahora // 100) % 2 == 0)
    if mostrar_jugador:
        if not dibujar_sprite(pantalla, sprites, "player", jugador_pantalla, (255, 235, 190)):
            pygame.draw.rect(pantalla, COLOR_JUGADOR, jugador_pantalla, border_radius=8)
            pygame.draw.rect(pantalla, (75, 52, 40), jugador_pantalla, 2, border_radius=8)
            pygame.draw.circle(pantalla, (35, 35, 45),
                               (jugador_pantalla.centerx - 7, jugador_pantalla.y + 14), 3)
            pygame.draw.circle(pantalla, (35, 35, 45),
                               (jugador_pantalla.centerx + 7, jugador_pantalla.y + 14), 3)

    # El indicador nunca muestra un piso superior al máximo del juego.
    piso = min(MAX_PISOS, int(estado["altura_maxima"] / ALTURA_POR_PISO))
    hud = pygame.Rect(12, 12, 300, 106)
    dibujar_panel_hud(pantalla, hud, textura_hud)
    dibujar_texto(pantalla, fuente_pequena, "Puntos: {}".format(estado["puntaje"]), 25, 22)
    dibujar_texto(pantalla, fuente_pequena, "Vidas: {}".format(estado["vidas"]), 25, 48)
    dibujar_texto(pantalla, fuente_pequena, "Piso: {}".format(piso), 25, 74)

    if ahora < estado["escudo_hasta"]:
        texto_poder = "Escudo activo"
    elif ahora < estado["salto_alto_hasta"]:
        texto_poder = "Super Bunny Jump activo"
    elif estado["puede_controlar_tiempo"]:
        texto_poder = "R: Control del tiempo"
    elif estado["puede_teletransportarse"]:
        texto_poder = "T: Teletransporte"
    else:
        texto_poder = ""
    if texto_poder:
        # Alinear el estado de poder al margen derecho.
        superficie = fuente_pequena.render(texto_poder, True, COLOR_TEXTO)
        pantalla.blit(superficie, (ANCHO - superficie.get_width() - 18, 18))

    # Indicador vertical sencillo de progreso hacia la altura objetivo.
    barra = pygame.Rect(ANCHO - 26, 80, 12, 220)
    pygame.draw.rect(pantalla, (45, 48, 64), barra, border_radius=5)
    progreso = min(1.0, estado["altura_maxima"] / float(ALTURA_META))
    alto_progreso = int(barra.h * progreso)
    if alto_progreso > 0:
        relleno = pygame.Rect(barra.x, barra.bottom - alto_progreso, barra.w, alto_progreso)
        pygame.draw.rect(pantalla, (205, 80, 105), relleno, border_radius=5)

    if ahora < estado["tiempo_detenido_hasta"]:
        dibujar_texto(pantalla, fuente, "TIEMPO DETENIDO", ANCHO // 2, 35,
                      (110, 230, 220), centrado=True)


def dibujar_fin(pantalla, fuentes, estado, ranking, nombre, ingresando_nombre=False):
    """Muestra el resultado y una lista del ranking."""
    dibujar_fondo(pantalla)
    fuente_titulo, fuente, fuente_pequena = fuentes
    titulo = "¡ESCAPASTE!" if estado["victoria"] else "GAME OVER"
    color_titulo = (110, 220, 155) if estado["victoria"] else (230, 90, 105)
    dibujar_texto(pantalla, fuente_titulo, titulo, ANCHO // 2, 35,
                  color_titulo, centrado=True)
    dibujar_texto(pantalla, fuente, estado["motivo_fin"], ANCHO // 2, 95,
                  COLOR_TEXTO, centrado=True)
    piso_final = min(MAX_PISOS, int(estado["altura_maxima"] / ALTURA_POR_PISO))
    dibujar_texto(pantalla, fuente, "Puntaje: {}   Piso: {}".format(
        estado["puntaje"], piso_final),
        ANCHO // 2, 135, COLOR_TEXTO, centrado=True)

    if ingresando_nombre:
        dibujar_texto(pantalla, fuente, "Escribe tu nombre y pulsa ENTER:",
                      ANCHO // 2, 205, COLOR_SECUNDARIO, centrado=True)
        dibujar_texto(pantalla, fuente_titulo, nombre if nombre else "_",
                      ANCHO // 2, 248, (245, 190, 90), centrado=True)
        return

    dibujar_texto(pantalla, fuente, "MEJORES 5", ANCHO // 2, 202,
                  (220, 90, 105), centrado=True)
    for indice, fila in enumerate(ranking[:5]):
        nombre, puntaje, fecha, piso = fila
        linea = "{}. {}  |  {} pts  |  piso {}".format(indice + 1, nombre, puntaje, piso)
        dibujar_texto(pantalla, fuente_pequena, linea, ANCHO // 2, 246 + indice * 29,
                      COLOR_TEXTO, centrado=True)

    dibujar_texto(pantalla, fuente_pequena,
                  "R: volver a jugar    M: menú    ESC: salir",
                  ANCHO // 2, 430, COLOR_SECUNDARIO, centrado=True)


# ============================================================================
# 6. LÓGICA DE MOVIMIENTO, COLISIONES Y PODERES
# ============================================================================

def aplicar_danio(estado, ahora, motivo, sonidos=None):
    """Resta una vida si el personaje no está protegido ni invulnerable."""
    protegido = ahora < estado["escudo_hasta"]
    invulnerable = ahora < estado["invulnerable_hasta"]
    if protegido or invulnerable:
        return

    estado["vidas"] -= 1
    reproducir_efecto(sonidos, "vida")
    estado["invulnerable_hasta"] = ahora + 1300
    estado["motivo_fin"] = motivo

    # Un golpe empuja al jugador hacia arriba un poco para separarlo del peligro.
    estado["velocidad_y"] = min(estado["velocidad_y"], -5.5)

    if estado["vidas"] <= 0:
        estado["victoria"] = False
        estado["motivo_fin"] = "Te quedaste sin vidas."


def recoger_poder(estado, poder, ahora):
    """Aplica el efecto del power-up recogido por el jugador."""
    tipo = poder["tipo"]
    if tipo == "escudo":
        estado["escudo_hasta"] = ahora + DURACION_ESCUDO
    elif tipo == "salto":
        estado["salto_alto_hasta"] = ahora + DURACION_SALTO_ALTO
    elif tipo == "vida":
        estado["vidas"] += 1
    elif tipo == "tiempo":
        if not estado["tiempo_ya_usado"]:
            estado["puede_controlar_tiempo"] = True
    elif tipo == "teletransporte":
        if not estado["teletransporte_ya_usado"]:
            estado["puede_teletransportarse"] = True


def activar_teletransporte(estado):
    """Coloca al personaje sobre una plataforma que esté por encima de él."""
    jugador = estado["jugador"]
    plataformas_superiores = [
        plataforma for plataforma in estado["plataformas"]
        if plataforma.y < jugador.y - 100
    ]
    if not plataformas_superiores:
        return

    # Escogemos una de las plataformas superiores más cercanas en altura.
    objetivo = max(plataformas_superiores, key=lambda plataforma: plataforma.y)
    jugador.centerx = objetivo.centerx
    jugador.bottom = objetivo.top
    estado["velocidad_y"] = 0
    estado["en_plataforma"] = True
    estado["puede_teletransportarse"] = False


def actualizar_partida(estado, teclas, teclas_presionadas, ahora, sonidos=None):
    """Actualiza una partida durante un cuadro (frame)."""
    jugador = estado["jugador"]
    velocidad_salto = FUERZA_SALTO
    if ahora < estado["salto_alto_hasta"]:
        velocidad_salto *= 1.35

    # Movimiento lateral. La envoltura hace que el jugador reaparezca por el
    # otro lado al salir del borde, como en el ejemplo de la profesora.
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        jugador.x -= VELOCIDAD_HORIZONTAL
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        jugador.x += VELOCIDAD_HORIZONTAL
    if jugador.right < 0:
        jugador.left = ANCHO
    elif jugador.left > ANCHO:
        jugador.right = 0

    # El salto solo se permite desde una plataforma y se inicia al presionar
    # la tecla, no por mantenerla apretada.
    if teclas_presionadas and estado["en_plataforma"]:
        estado["velocidad_y"] = velocidad_salto
        estado["en_plataforma"] = False

    # Caída por gravedad y movimiento vertical.
    y_anterior = jugador.y
    estado["velocidad_y"] += GRAVEDAD
    jugador.y += int(estado["velocidad_y"])
    estado["en_plataforma"] = False

    # Solo se aterriza en una plataforma al caer, nunca al subir desde abajo.
    if estado["velocidad_y"] > 0:
        pie_anterior = y_anterior + jugador.h
        for plataforma in estado["plataformas"]:
            cruza_plataforma = (
                pie_anterior <= plataforma.top + 3
                and jugador.bottom >= plataforma.top
            )
            esta_encima = jugador.right > plataforma.left and jugador.left < plataforma.right
            if cruza_plataforma and esta_encima:
                jugador.bottom = plataforma.top
                estado["velocidad_y"] = 0
                estado["en_plataforma"] = True
                break

    # Cámara vertical: sigue al personaje al subir, sin volver hacia abajo.
    posicion_pantalla_y = jugador.y - estado["camara_y"]
    if posicion_pantalla_y < ALTO * 0.40:
        estado["camara_y"] = jugador.y - ALTO * 0.40

    # Guardamos la mejor altura alcanzada sin superar la meta del piso 100.
    # El piso 0 es el inicio; el piso 100 corresponde a ALTURA_META.
    altura_desde_inicio = min(ALTURA_META, max(0, int(520 - jugador.y)))
    if altura_desde_inicio > estado["altura_maxima"]:
        estado["altura_maxima"] = altura_desde_inicio

    # Los monstruos aparecen aleatoriamente por encima de la zona visible y caen.
    # El poder de detener el tiempo pausa su aparición y su movimiento.
    if ahora >= estado["tiempo_detenido_hasta"]:
        # El intervalo, la posición horizontal y la velocidad se sortean para
        # que las apariciones no ocurran siempre de la misma manera.
        if ahora >= estado["proximo_enemigo_ms"]:
            tamano = random.randint(30, 38)
            enemigo = {
                "rect": pygame.Rect(
                    random.randint(0, ANCHO - tamano),
                    int(estado["camara_y"] - tamano),
                    tamano,
                    tamano,
                ),
                "velocidad": random.randint(
                    VELOCIDAD_ENEMIGO_MIN,
                    VELOCIDAD_ENEMIGO_MAX,
                ),
            }
            estado["enemigos_caida"].append(enemigo)
            estado["proximo_enemigo_ms"] = ahora + random.randint(
                INTERVALO_ENEMIGO_MIN,
                INTERVALO_ENEMIGO_MAX,
            )

        # Los enemigos caen atravesando la escena y se eliminan al salir por
        # debajo de la pantalla para que la lista no crezca indefinidamente.
        for enemigo in estado["enemigos_caida"][:]:
            enemigo["rect"].y += enemigo["velocidad"]
            if enemigo["rect"].top - estado["camara_y"] > ALTO + 45:
                estado["enemigos_caida"].remove(enemigo)

    # Frascos y power-ups se retiran al tocarlos para evitar sumarlos repetidamente.
    for frasco in estado["frascos"][:]:
        if jugador.colliderect(frasco):
            estado["frascos"].remove(frasco)
            estado["puntaje"] += 10
            reproducir_efecto(sonidos, "punto")

    for poder in estado["poderes"][:]:
        if jugador.colliderect(poder["rect"]):
            recoger_poder(estado, poder, ahora)
            estado["poderes"].remove(poder)

    # Los monstruos que caen descuentan una vida con breve invulnerabilidad
    # para evitar perder varias vidas en un mismo choque.
    for enemigo in estado["enemigos_caida"][:]:
        if jugador.colliderect(enemigo["rect"]):
            aplicar_danio(
                estado,
                ahora,
                "Un monstruo cayó desde arriba y te alcanzó.",
                sonidos,
            )
            estado["enemigos_caida"].remove(enemigo)
            break

    # Condición de victoria provisional por altura alcanzada.
    if estado["altura_maxima"] >= ALTURA_META:
        estado["victoria"] = True
        estado["motivo_fin"] = "Llegaste a la cima del edificio."

    # Si el jugador cae por debajo del área visible, pierde la partida.
    if jugador.top - estado["camara_y"] > ALTO:
        estado["victoria"] = False
        estado["motivo_fin"] = "Caíste fuera del edificio."


def activar_poderes(estado, evento, ahora):
    """Activa los poderes que requieren pulsar una tecla."""
    if evento.key == pygame.K_r and estado["puede_controlar_tiempo"]:
        estado["tiempo_detenido_hasta"] = ahora + DURACION_TIEMPO_DETENIDO
        estado["puede_controlar_tiempo"] = False
        estado["tiempo_ya_usado"] = True
    elif evento.key == pygame.K_t and estado["puede_teletransportarse"]:
        activar_teletransporte(estado)
        estado["teletransporte_ya_usado"] = True


# ============================================================================
# 7. CICLO PRINCIPAL Y MANEJO DE PANTALLAS
# ============================================================================

def main():
    """Inicia Pygame y administra menú, partida, ayuda y ranking."""
    pygame.init()
    sonidos = cargar_sonidos()
    iniciar_musica(sonidos)
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("JUST CLIMB — prototipo")
    reloj = pygame.time.Clock()
    textura_hud = cargar_panel_hud()
    sprites = cargar_sprites()

    fuentes = cargar_fuentes()

    # La tabla se crea al iniciar, aunque el jugador todavía no haya terminado
    # una partida. Así la pantalla de ranking puede abrirse sin errores.
    preparar_base_datos()

    pantalla_actual = "menu"
    seleccion_menu = 0
    estado = nuevo_estado_partida()
    nombre_jugador = ""
    nombre_guardado = False
    ranking = obtener_mejores_puntajes()
    corriendo = True

    while corriendo:
        reloj.tick(FPS)
        ahora = pygame.time.get_ticks()
        teclas = pygame.key.get_pressed()
        salto_presionado = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            elif evento.type == pygame.KEYDOWN:
                if pantalla_actual == "menu":
                    if evento.key in (pygame.K_UP, pygame.K_w):
                        seleccion_menu = (seleccion_menu - 1) % 3
                    elif evento.key in (pygame.K_DOWN, pygame.K_s):
                        seleccion_menu = (seleccion_menu + 1) % 3
                    elif evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if seleccion_menu == 0:
                            estado = nuevo_estado_partida()
                            pantalla_actual = "juego"
                            iniciar_musica(sonidos)
                        elif seleccion_menu == 1:
                            pantalla_actual = "ayuda"
                        else:
                            corriendo = False

                elif pantalla_actual == "ayuda":
                    if evento.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                        pantalla_actual = "menu"

                elif pantalla_actual == "juego":
                    if evento.key == pygame.K_SPACE:
                        salto_presionado = True
                    activar_poderes(estado, evento, ahora)

                elif pantalla_actual == "ingreso_nombre":
                    if evento.key == pygame.K_RETURN:
                        guardar_puntaje(nombre_jugador, estado["puntaje"],
                                        int(estado["altura_maxima"] / ALTURA_POR_PISO))
                        nombre_guardado = True
                        ranking = obtener_mejores_puntajes()
                        pantalla_actual = "resultado"
                    elif evento.key == pygame.K_BACKSPACE:
                        nombre_jugador = nombre_jugador[:-1]
                    elif evento.unicode and evento.unicode.isprintable() and len(nombre_jugador) < 20:
                        nombre_jugador += evento.unicode

                elif pantalla_actual == "resultado":
                    if evento.key == pygame.K_r:
                        estado = nuevo_estado_partida()
                        nombre_jugador = ""
                        nombre_guardado = False
                        pantalla_actual = "juego"
                        iniciar_musica(sonidos)
                    elif evento.key == pygame.K_m:
                        pantalla_actual = "menu"
                        iniciar_musica(sonidos)
                    elif evento.key == pygame.K_ESCAPE or evento.key == pygame.K_q:
                        corriendo = False

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if pantalla_actual == "menu":
                    botones = [pygame.Rect(ANCHO // 2 - 150, 275 + i * 68, 300, 50)
                               for i in range(3)]
                    for indice, rect in enumerate(botones):
                        if rect.collidepoint(evento.pos):
                            if indice == 0:
                                estado = nuevo_estado_partida()
                                pantalla_actual = "juego"
                                iniciar_musica(sonidos)
                            elif indice == 1:
                                pantalla_actual = "ayuda"
                            else:
                                corriendo = False

        # Actualizar el juego solo cuando está en curso.
        if pantalla_actual == "juego":
            actualizar_partida(estado, teclas, salto_presionado, ahora, sonidos)
            if estado["vidas"] <= 0 or estado["victoria"] or estado["motivo_fin"] == "Caíste fuera del edificio.":
                detener_musica()
                # El efecto de Game Over se usa al perder, no al alcanzar la meta.
                if not estado["victoria"]:
                    reproducir_efecto(sonidos, "game_over")
                pantalla_actual = "ingreso_nombre"

        # Dibujar la pantalla actual.
        if pantalla_actual == "menu":
            dibujar_menu(pantalla, fuentes, seleccion_menu)
        elif pantalla_actual == "ayuda":
            dibujar_ayuda(pantalla, fuentes)
        elif pantalla_actual == "juego":
            dibujar_partida(pantalla, fuentes, estado, ahora, textura_hud, sprites)
        elif pantalla_actual == "ingreso_nombre":
            dibujar_fin(pantalla, fuentes, estado, ranking, nombre_jugador, True)
        elif pantalla_actual == "resultado":
            dibujar_fin(pantalla, fuentes, estado, ranking, nombre_jugador, False)

        pygame.display.flip()

    pygame.quit()


# ============================================================================
# 8. PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================================

if __name__ == "__main__":
    main()
