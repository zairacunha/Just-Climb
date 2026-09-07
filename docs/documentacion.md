# Documentación del juego — JUST CLIMB

## 2.1. Descripción general del juego

**JUST CLIMB** es un juego 2D de plataformas con temática de horror. El jugador
controla a un experimento creado en un laboratorio clandestino. La partida
comienza en el subsuelo de un edificio abandonado, identificado como el piso 0.

El objetivo principal es escapar del edificio subiendo por plataformas que
aparecen aleatoriamente. Durante el recorrido, el jugador debe esquivar monstruos
y objetos peligrosos que caen desde las partes superiores del edificio.

Para avanzar, el jugador puede moverse hacia la izquierda y hacia la derecha con
las flechas del teclado y saltar utilizando la barra espaciadora. También puede
recolectar frascos para aumentar su puntaje y obtener distintos power-ups.

El juego termina cuando el jugador pierde sus 3 vidas o cuando realiza un salto
incorrecto y cae nuevamente hasta el piso 0. Si logra llegar hasta la cima del
edificio sin caer y sin perder todas sus vidas, gana la partida y consigue
escapar.

---

## 2.2. Detalle de la mecánica del juego

### Personaje

El jugador controla a un experimento creado en un laboratorio clandestino. La
partida comienza en el subsuelo del edificio, correspondiente al piso 0.

El objetivo del personaje es subir por el edificio utilizando las plataformas
que aparecen en el escenario y llegar hasta la cima para escapar.

### Controles

| Acción | Control |
|---|---|
| Moverse hacia la izquierda | Flecha izquierda |
| Moverse hacia la derecha | Flecha derecha |
| Saltar | Barra espaciadora |
| Seleccionar una opción del menú | Mouse o flechas del teclado |
| Confirmar una opción | Mouse o tecla correspondiente |

### Plataformas

Las plataformas aparecen en posiciones aleatorias a medida que el jugador
avanza. El jugador debe calcular correctamente sus saltos para aterrizar sobre
ellas y continuar subiendo.

Si el jugador realiza un salto incorrecto y cae nuevamente hasta el piso 0, la
partida termina.

### Monstruos y objetos peligrosos

Durante el ascenso aparecen monstruos y objetos peligrosos que caen desde la
parte superior del edificio. El jugador debe esquivarlos para evitar recibir
daño.

Cada vez que el jugador recibe daño de un monstruo o de un objeto peligroso,
pierde una vida.

### Vidas

El jugador comienza cada partida con 3 vidas.

Las vidas se pierden cuando el jugador recibe daño de los monstruos o de los
objetos peligrosos. La partida termina cuando el jugador pierde las 3 vidas.

El power-up “A Second Chance” puede otorgar una vida adicional, pero solo puede
aparecer una vez durante la partida.

### Puntaje

El jugador obtiene puntos al recolectar frascos que aparecen en el escenario.

El puntaje actual se muestra durante la partida mediante el HUD. Al finalizar,
el puntaje se solicita junto con el nombre del jugador y se guarda en la base de
datos SQLite para formar parte del ranking.

### Power-ups

#### Not This Time

Es un escudo protector.

- Evita que el jugador reciba daño de los monstruos y objetos peligrosos.
- Tiene una duración de 10 segundos.
- No evita que el jugador muera si cae hasta el piso 0.

#### Super Bunny Jump

Aumenta la capacidad de salto del jugador.

- Permite saltar más alto de lo normal.
- Tiene una duración de 5 minutos.

#### A Second Chance

Es un power-up especial que otorga una vida adicional.

- Puede aparecer durante la partida.
- Solo aparece una vez.
- Permite continuar jugando después de perder una vida.

#### Time Control

Permite detener temporalmente el tiempo del juego.

- El jugador puede detener el tiempo.
- Solo puede utilizarse una vez.
- Recolectar más de un power-up de este tipo no permite utilizarlo más veces.

#### Get Me Out Of Here

Permite que el jugador se teletransporte hacia otra plataforma.

- Ayuda a escapar de una situación peligrosa.
- Solo puede utilizarse una vez durante la partida.

### Condiciones de Game Over

La partida puede terminar de dos maneras:

1. El jugador pierde sus 3 vidas debido al daño recibido de monstruos u objetos
   peligrosos.
2. El jugador realiza un salto mal calculado y cae nuevamente hasta el piso 0.

### Condición de victoria

El jugador gana cuando logra llegar hasta la cima del edificio sin caer y sin
perder todas sus vidas.

Al ganar, el juego debe mostrar una pantalla que indique que el experimento
logró escapar del edificio.

---

## 2.3. Pantallas a crear

### Pantalla de Inicio

**Qué muestra:**

- El título “JUST CLIMB”.
- La ambientación del laboratorio clandestino o del edificio abandonado.
- Las opciones “Escape”, “Help” y “Give Up”.

**Qué se puede hacer:**

- Seleccionar “Escape” para comenzar.
- Seleccionar “Help” para consultar los controles y power-ups.
- Seleccionar “Give Up” para salir del juego.

**Controles:**

- Cursor del mouse.
- Flechas del teclado.
- Botón o tecla de confirmación.

**Estética:**

- Fondo oscuro.
- Colores relacionados con el horror, como rojo, negro y violeta.
- Iluminación tenue y elementos visuales de un edificio abandonado.

### Pantalla de ayuda

**Qué muestra:**

- Los controles del personaje.
- La función de cada power-up.
- Una explicación breve de cómo subir por el edificio.
- Las condiciones de Game Over y de victoria.

**Qué se puede hacer:**

- Leer las instrucciones.
- Volver a la pantalla de inicio.

**Controles:**

- Flechas del teclado o cursor del mouse.
- Botón para volver.

### Pantalla de Juego

**Qué muestra:**

- El personaje.
- Las plataformas.
- Los monstruos.
- Los objetos peligrosos.
- Los frascos.
- Los power-ups.
- El piso actual.
- El puntaje.
- Las vidas restantes.

**Qué se puede hacer:**

- Moverse hacia la izquierda y hacia la derecha.
- Saltar.
- Recolectar frascos.
- Obtener y utilizar power-ups.
- Subir por las plataformas.

**Estética:**

- Escenario oscuro con ambientación de horror.
- Plataformas distribuidas verticalmente.
- Monstruos y objetos peligrosos con colores contrastantes para que puedan
  identificarse.

### Pantalla de Game Over

**Qué muestra:**

- El texto “GAME OVER”.
- El motivo por el que terminó la partida.
- El puntaje final.
- El piso alcanzado.
- Una indicación para ingresar el nombre del jugador.

**Qué se puede hacer:**

- Escribir el nombre del jugador.
- Confirmar el guardado del puntaje.
- Continuar hacia el ranking.

### Pantalla de Victoria

**Qué muestra:**

- Un mensaje indicando que el jugador escapó del edificio.
- El puntaje final.
- El piso alcanzado.
- Una indicación para ingresar el nombre del jugador.

**Qué se puede hacer:**

- Escribir el nombre del jugador.
- Confirmar el guardado del puntaje.
- Continuar hacia el ranking.

### Pantalla de Ranking

**Qué muestra:**

- Los 5 mejores puntajes.
- El nombre de cada jugador.
- El puntaje obtenido.
- La fecha de la partida, si corresponde.

**Qué se puede hacer:**

- Consultar los récords.
- Elegir volver a jugar.
- Elegir salir del juego.

### Pantalla Fin

**Qué muestra:**

- Un mensaje de despedida o confirmación de salida.

**Qué se puede hacer:**

- Cerrar el juego.
- Volver a la pantalla de inicio, si esa opción se implementa.

---

## 2.4. Estructura de la base de datos SQLite

El juego utilizará una base de datos SQLite para guardar los puntajes obtenidos
por los jugadores.

### Tabla `ranking`

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | Identificador único del registro |
| `nombre` | TEXT NOT NULL | Nombre ingresado por el jugador |
| `puntaje` | INTEGER NOT NULL | Puntaje obtenido durante la partida |
| `fecha` | TEXT NOT NULL | Fecha en la que se jugó la partida |
| `piso` | INTEGER NOT NULL | Piso máximo alcanzado |

### Sentencia SQL de creación

```sql
CREATE TABLE IF NOT EXISTS ranking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    puntaje INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    piso INTEGER NOT NULL
);
