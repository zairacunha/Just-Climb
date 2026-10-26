
from db import guardar_puntaje, init_db, obtener_top


def main():
    # Crea la tabla antes de guardar o consultar puntajes.
    init_db()

    # Pide los datos de un puntaje nuevo.
    nombre = input("Escribe el nombre: ").strip()

    try:
        puntaje = int(input("Escribe el puntaje: "))
    except ValueError:
        print("El puntaje debe ser un número entero.")
        return

    # Guarda el puntaje usando la función del módulo db.py.
    try:
        guardar_puntaje(nombre, puntaje)
    except ValueError as error:
        print(error)
        return

    # Recupera y muestra los cinco mejores puntajes.
    mejores_puntajes = obtener_top(5)

    print("\nTop 5 puntajes:")
    for posicion, (nombre, puntaje) in enumerate(mejores_puntajes, start=1):
        print(f"{posicion}. {nombre}: {puntaje}")


if __name__ == "__main__":
    main()
