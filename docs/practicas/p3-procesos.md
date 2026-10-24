# Práctica 3 · Procesos y prioridades

[Descargar el enunciado en PDF](pdf/UT3_P3_Procesos.pdf){ .md-button .md-button--primary }

| | |
|---|---|
| **Apartados de los apuntes** | 3.7 Procesos · 3.8 Prioridad de procesos |
| **Entorno** | Máquina virtual Ubuntu (mejor con **2 CPU** asignadas en VirtualBox) |
| **Entrega** | `UT3_P3_Apellido_Nombre.pdf` |

## Objetivo

Gestionar trabajos en primer y segundo plano, supervisar los procesos del sistema, enviarles señales y modificar su prioridad.

## Qué hay que entregar

Una memoria en PDF con, para cada ejercicio, el **comando** (como texto), una **captura** del resultado con tu *prompt* y la **respuesta razonada** a las preguntas.

!!! warning "Haz esta práctica en la máquina virtual"
    En la parte C vas a poner la CPU al 100 %. No la hagas en el equipo del aula.

## Parte A · Trabajos

1. Lanza `sleep 900` en primer plano. Suspéndelo, compruébalo con `jobs` y reanúdalo en segundo plano.
2. Lanza en segundo plano `sleep 1100`, `sleep 1200` y `sleep 1300`. Muestra la lista de trabajos con sus PID.
3. Trae a primer plano el trabajo `sleep 1200` **sin usar su número**, y termínalo desde el teclado.
4. ¿Qué diferencia hay entre el número de trabajo (`%1`) y el PID? ¿Puedes ver los trabajos de esta terminal desde otra terminal con `jobs`? ¿Y con `ps`?
5. Abre el editor `nano` sobre un fichero cualquiera, suspéndelo y comprueba en qué estado aparece con `ps`. Vuelve a él y ciérralo.

## Parte B · Supervisar procesos

6. Muestra todos los procesos del sistema con el estilo BSD y con el estilo UNIX. ¿Qué columnas aparecen en uno y no en el otro?
7. Muestra los procesos en forma de árbol. ¿Qué proceso tiene el PID 1? ¿Quién es el proceso padre de tu shell?
8. Muestra solo el PID, el usuario, el % de CPU, el % de memoria y el comando de los **5 procesos que más memoria** consumen.
9. ¿Cuántos procesos tiene en marcha `root`? ¿Y tu usuario?
10. Abre `top`:

    a) Explica qué indica cada línea de la cabecera.
    b) Ordena los procesos por memoria.
    c) Muestra solo los de tu usuario.
    d) Muestra el uso de cada CPU por separado.

11. ¿Cuál es la carga media de tu máquina? ¿Cuántos núcleos tiene? ¿Está sobrecargada?
12. Usa `watch` para ver cada 2 segundos la memoria libre del sistema mientras abres y cierras alguna aplicación pesada (por ejemplo, Firefox).

## Parte C · Señales y prioridades

13. Muestra la lista de señales disponibles. Explica para qué sirven `SIGTERM`, `SIGKILL`, `SIGHUP` y `SIGSTOP`.
14. Lanza `sleep 3000 &`. Detenlo con `SIGSTOP` y comprueba su estado con `ps`. Reanúdalo con `SIGCONT` y termínalo con `SIGTERM`, todo **usando su PID**.
15. Lanza varios `sleep` en segundo plano y termínalos todos con una sola orden **por nombre**. Hazlo de dos formas diferentes.
16. Lanza `yes > /dev/null &` tres veces. Comprueba en `top` cuánta CPU consume cada uno.
17. Lanza otros tres `yes > /dev/null &` con prioridad **mínima**. Compara en `top` el `%CPU` y las columnas `PR` y `NI` de los seis procesos. Explica lo que ves.
18. A uno de los tres primeros `yes`, súbele el valor *nice* a 10 con `renice`. Después intenta devolverlo a 0 sin `sudo`. ¿Qué ocurre? ¿Y con `sudo`?
19. Termina todos los procesos `yes` y comprueba que la carga de la CPU vuelve a la normalidad.

!!! question "Pregunta final"
    Un compañero tiene en el servidor del aula un proceso que lleva horas consumiendo el 100 % de la CPU y no sabes si está haciendo algo importante. ¿Qué harías antes de matarlo? ¿Qué señal usarías primero y por qué?
