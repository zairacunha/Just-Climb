
import sqlite3
from pathlib import Path


# Guarda ranking.db en la misma carpeta que db.py.
RUTA_DB = Path(__file__).resolve().parent / "ranking.db"


def init_db():
    # Crea la tabla de puntajes si todavía no existe.
    conexion = sqlite3.connect(RUTA_DB)

    try:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS puntajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                puntaje INTEGER NOT NULL
            )
        """)

        # Confirma la creación de la tabla.
        conexion.commit()
    finally:
        # Cierra la conexión a la base de datos.
        conexion.close()


def guardar_puntaje(nombre, puntaje):
    # Quita espacios sobrantes del principio y del final del nombre.
    nombre = nombre.strip()

    # Evita guardar nombres vacíos.
    if not nombre:
        raise ValueError("El nombre no puede estar vacío.")

    # Abre una conexión y guarda el nuevo puntaje.
    conexion = sqlite3.connect(RUTA_DB)

    try:
        # Los signos ? sustituyen los valores de forma segura.
        conexion.execute(
            "INSERT INTO puntajes (nombre, puntaje) VALUES (?, ?)",
            (nombre, puntaje),
        )

        # Confirma que el puntaje se haya guardado.
        conexion.commit()
    finally:
        # Cierra la conexión después de guardar.
        conexion.close()


def obtener_top(cantidad=5):
    # Rechaza cantidades cero o negativas.
    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor que cero.")

    conexion = sqlite3.connect(RUTA_DB)

    try:
        # Ordena los puntajes de mayor a menor y limita los resultados.
        cursor = conexion.execute("""
            SELECT nombre, puntaje
            FROM puntajes
            ORDER BY puntaje DESC
            LIMIT ?
        """, (cantidad,))

        # Devuelve una lista de tuplas: (nombre, puntaje).
        return cursor.fetchall()
    finally:
        # Cierra la conexión después de leer los datos.
        conexion.close()


def borrar_ranking():
    # Función opcional: elimina todos los puntajes guardados.
    conexion = sqlite3.connect(RUTA_DB)

    try:
        conexion.execute("DELETE FROM puntajes")
        conexion.commit()
    finally:
        conexion.close()
