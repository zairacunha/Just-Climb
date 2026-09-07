# 👻 JUST CLIMB

Juego 2D de plataformas con temática de horror, desarrollado en Python con
Pygame para el proyecto individual de la materia Software Factory II.

## Descripción

En JUST CLIMB, el jugador controla a un experimento creado en un laboratorio
clandestino. La partida comienza en el subsuelo de un viejo edificio, ubicado en
el piso 0.

El objetivo es escapar del edificio subiendo por plataformas que aparecen
aleatoriamente. Durante el recorrido, el jugador debe esquivar monstruos y
objetos peligrosos que caen desde las partes superiores.

También puede recolectar frascos para sumar puntos y conseguir power-ups con
habilidades especiales.

La partida termina si el jugador pierde sus 3 vidas o si realiza un salto
incorrecto y cae nuevamente hasta el piso 0. Si logra llegar hasta la cima sin
caer y sin perder todas sus vidas, gana y escapa del edificio.

## Cómo jugar

1. Ejecutar el juego.
2. En la pantalla de inicio, seleccionar **Escape** para comenzar.
3. Seleccionar **Help** para consultar los controles y los power-ups.
4. Seleccionar **Give Up** para salir del juego.
5. Usar la flecha izquierda para moverse hacia la izquierda.
6. Usar la flecha derecha para moverse hacia la derecha.
7. Presionar la barra espaciadora para saltar.
8. Esquivar los monstruos y los objetos peligrosos.
9. Recolectar los frascos para aumentar el puntaje.
10. Utilizar los power-ups para obtener ventajas.
11. Llegar hasta la cima del edificio para ganar.

## Controles

| Acción | Control |
|---|---|
| Moverse hacia la izquierda | Flecha izquierda |
| Moverse hacia la derecha | Flecha derecha |
| Saltar | Barra espaciadora |
| Seleccionar una opción | Mouse o flechas del teclado |
| Confirmar una opción | Mouse o tecla correspondiente |

## Power-ups

| Power-up | Efecto | Restricción |
|---|---|---|
| **Not This Time** | Protege del daño de monstruos y objetos. | Dura 10 segundos y no protege contra caídas. |
| **Super Bunny Jump** | Permite saltar más alto de lo normal. | Dura 5 minutos. |
| **A Second Chance** | Otorga una vida extra. | Solo aparece una vez. |
| **Time Control** | Permite detener el tiempo del juego. | Solo puede utilizarse una vez. |
| **Get Me Out Of Here** | Teletransporta al jugador hacia otra plataforma. | Solo puede utilizarse una vez. |

## Condiciones de la partida

### Game Over

La partida termina en cualquiera de estas situaciones:

- El jugador pierde sus 3 vidas por recibir daño.
- El jugador realiza un salto incorrecto y cae hasta el piso 0.

### Victoria

El jugador gana cuando llega hasta la cima del edificio sin caer y sin perder
todas sus vidas.

## Funcionalidades

- [x] Pantalla de inicio con las opciones `Escape`, `Help` y `Give Up`
- [x] Pantalla de ayuda con controles y power-ups
- [x] Movimiento horizontal del personaje
- [x] Salto con la barra espaciadora
- [x] Plataformas generadas aleatoriamente
- [x] Monstruos y objetos peligrosos
- [x] Sistema de 3 vidas
- [x] Recolección de frascos
- [x] Sistema de puntaje
- [x] Power-up `Not This Time`
- [x] Power-up `Super Bunny Jump`
- [x] Power-up `A Second Chance`
- [x] Power-up `Time Control`
- [x] Power-up `Get Me Out Of Here`
- [x] HUD con puntaje, vidas y piso actual
- [x] Pantalla de Game Over
- [x] Pantalla de victoria
- [x] Solicitud del nombre del jugador al finalizar
- [x] Ranking con los 5 mejores puntajes
- [x] Guardado de puntajes en SQLite
- [x] Opción de volver a jugar o salir

> Las funcionalidades se irán verificando y ajustando a medida que avance la
> implementación del juego.

## Capturas de pantalla

Las capturas de pantalla se agregarán cuando el juego tenga una primera versión
jugable.

## Cómo ejecutar

### Requisitos previos

- Python 3.8 o superior.
- Pygame.
- Git.

### Clonar el repositorio

```bash
git clone git@github.com:zairacunha/Just-Climb.git
cd just-climb

```
## Estado del proyecto

🔨 En desarrollo

## Autor

Zaira Cunha da Silva - @zairacunha
