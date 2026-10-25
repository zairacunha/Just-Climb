
import sqlite3
from pathlib import Path


# Guarda la base de datos junto a este archivo .py.
RUTA_DB = Path(__file__).resolve().parent / "ranking.db"


def main():
    # Abre una conexión con la base de datos.
    conexion = sqlite3.connect(RUTA_DB)

    try:
        # Crea la tabla si todavía no existe.
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS puntajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                puntaje INTEGER NOT NULL
            )
        """)

        # Inserta tres puntajes de ejemplo usando placeholders.
        puntajes_ejemplo = [
            ("Ana", 1500),
            ("Luis", 1200),
            ("Marta", 1800),
        ]

        conexion.executemany(
            "INSERT INTO puntajes (nombre, puntaje) VALUES (?, ?)",
            puntajes_ejemplo,
        )

        # Guarda los cambios en la base de datos.
        conexion.commit()

        # Consulta los tres puntajes más altos.
        cursor = conexion.execute("""
            SELECT nombre, puntaje
            FROM puntajes
            ORDER BY puntaje DESC
            LIMIT 3
        """)

        mejores_puntajes = cursor.fetchall()

        # Muestra el ranking en la consola.
        print("Top 3 puntajes:")
        for posicion, (nombre, puntaje) in enumerate(mejores_puntajes, start=1):
            print(f"{posicion}. {nombre}: {puntaje}")

    finally:
        # Cierra la conexión aunque ocurra un error.
        conexion.close()


if __name__ == "__main__":
    main()
