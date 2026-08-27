# Diagrama de Flujo — Just Climb

## Descripción

Este diagrama muestra las pantallas principales de Just Climb y las transiciones entre ellas. El jugador comienza en la pantalla de inicio, luego juega hasta perder por quedarse sin vidas o caer fuera del escenario. Al finalizar la partida, el puntaje se guarda en SQLite y se muestra el ranking.

## Pantallas

| Pantalla | Descripción | Cómo se llega |
|---|---|---|
| Inicio | Muestra el título Just Climb y la opción para comenzar. | Al abrir el programa |
| Juego | Muestra al personaje, plataformas, monstruos, objetos, frascos, power-ups y HUD. | Al seleccionar "Jugar" |
| Game Over | Muestra el motivo de la derrota y el puntaje final. | Al perder las 3 vidas o caer del escenario |
| Ranking | Muestra los 5 mejores puntajes guardados. | Después de la pantalla de Game Over |
| Fin | Muestra las opciones para volver a jugar o salir. | Después de consultar el ranking |

## Transiciones

| Desde | Evento | Hacia |
|---|---|---|
| Inicio | Presionar "Jugar" o la tecla indicada | Juego |
| Juego | El jugador pierde una vida | Juego |
| Juego | Las vidas llegan a 0 | Game Over |
| Juego | El jugador cae fuera del escenario | Game Over |
| Juego | El jugador cierra la ventana | Fin |
| Game Over | Se guarda el puntaje en SQLite | Ranking |
| Ranking | Presionar "Jugar de nuevo" | Juego |
| Ranking | Presionar "Salir" | Fin |
| Fin | Confirmar la salida | Se cierra el programa |

## Diagrama visual

```mermaid
flowchart TD
    A[Inicio] -->|Presionar Jugar| B[Juego]

    B -->|Recolectar frascos| B
    B -->|Obtener power-ups| B
    B -->|Subir de piso| B
    B -->|Tocar monstruo u objeto peligroso| C{¿Quedan vidas?}

    C -->|Sí| B
    C -->|No| D[Game Over]

    B -->|Caer fuera del escenario| D

    D -->|Guardar puntaje en SQLite| E[Ranking]
    E -->|Jugar de nuevo| B
    E -->|Salir| F[Fin]

    F -->|Cerrar programa| G[Programa cerrado]
