# Práctica 2 · Comodines, redirecciones y búsqueda de ficheros

[Descargar el enunciado en PDF](pdf/UT3_P2_Comodines.pdf){ .md-button .md-button--primary }

| | |
|---|---|
| **Apartados de los apuntes** | 3.3 Comodines · 3.4 `find` · 3.5 Redirecciones |
| **Entorno** | Máquina virtual Ubuntu |
| **Entrega** | `UT3_P2_Apellido_Nombre.pdf` |

## Objetivo

Seleccionar grupos de ficheros con comodines, controlar adónde van la salida y los errores de los comandos, y localizar ficheros con `find` según su nombre, tipo, tamaño y fecha.

## Qué hay que entregar

Una memoria en PDF con, para cada ejercicio, el **comando** (como texto), una **captura** del resultado con tu *prompt* y la **respuesta razonada** a las preguntas.

Trabaja dentro de `~/PRACTICA2`, que debes crear al empezar.

## Parte A · Comodines

Lista (solo con `ls` y comodines, sin `grep`):

1. Todos los ficheros de `/bin`.
2. Los ficheros de `/etc` que empiezan por `t`, en orden inverso.
3. Los ficheros de `/etc` que **no** empiezan por `t`.
4. Los ficheros de `/dev` que empiezan por `tty` y tienen exactamente **5** caracteres.
5. Los ficheros de `/dev` que empiezan por `tty` y acaban en `1`, `2`, `3` o `4`.
6. Los ficheros de `/dev` que empiezan por `tty` y acaban en un número de **dos** cifras.
7. Los ficheros de `/usr/bin` cuyo nombre tiene exactamente **cuatro** letras y una `a` como segunda letra.
8. Los ficheros de `/etc` que contienen un número en cualquier posición del nombre.
9. Todos los ficheros (incluidos los ocultos) del directorio raíz.

Ahora con copias:

10. Crea en `PRACTICA2` los directorios `cuatro_letras` y `terminales`. Copia en `cuatro_letras` los ficheros del ejercicio 7.
11. Crea en `terminales` ficheros vacíos con el **mismo nombre** que los ficheros de `/dev` que empiezan por `tty`, acaban en una letra entre `a` y `f` y tienen cinco caracteres. (No copies los dispositivos: crea ficheros vacíos con `touch`.) Si en tu sistema no hay ninguno, crea tú mismo `ttyAa`, `ttyBb`, `ttyqc`, `ttyqf` y `ttyRb`.
12. Borra de `terminales` los ficheros que **no** acaben en `b` y tengan una `q` como cuarta letra.

!!! tip "Prueba antes de borrar"
    Antes de cualquier `rm` con comodines, ejecuta el mismo patrón con `ls` y comprueba qué se va a borrar. Incluye esa comprobación en la memoria.

## Parte B · Redirecciones

13. Guarda en `PRACTICA2/listado` el listado de `/tmp`.
14. **Añade** al final de `listado` el listado de los ficheros de `/etc` que empiezan por `t`. Comprueba que no se ha perdido lo anterior.
15. Ejecuta `ls /etc/hostname /etc/noexiste`. Haz que la salida correcta vaya a `bien.txt` y el error a `errores.txt`.
16. Repite el ejercicio anterior para que **todo** (salida y errores) vaya a `todo.txt`. Hazlo de dos formas distintas.
17. Muestra el día y la hora actuales y **añádelos** a un fichero `registro.log`. Repítelo tres veces y comprueba que el fichero tiene tres líneas.
18. Usando un *here document*, crea el fichero `ficha.txt` con tu nombre, tu usuario del sistema (con una variable), tu directorio personal (con una variable) y la fecha de hoy. (Pista: dentro del texto, `$(date +%d/%m/%Y)` se sustituye por la fecha; lo veremos en el apartado 3.6.)
19. Activa la protección `noclobber` y demuestra que impide sobrescribir `ficha.txt`. Desactívala.

## Parte C · Buscar ficheros con `find`

20. Busca en tu directorio personal todos los ficheros **ordinarios** (no directorios) y muéstralos.
21. Busca en tu directorio personal todos los ficheros cuyo nombre contenga `practica` sin distinguir mayúsculas.
22. Busca en `/home` todos los ficheros de más de 100 MB. Evita que aparezcan errores de permisos.
23. Busca en `/var/log` los ficheros modificados en las últimas 24 horas.
24. Busca en `/etc` los directorios (solo directorios) cuyo nombre acabe en `.d`, sin bajar más de un nivel.
25. Busca en tu directorio personal los ficheros vacíos.
26. Busca en `PRACTICA2` todos los `.txt` y, con `-exec`, muestra el tamaño de cada uno con `ls -lh`.
27. Busca en tu directorio personal los ficheros que **contengan** la palabra `práctica` en su interior (no en el nombre). Pista: combina `find` con `grep`.

!!! question "Pregunta final"
    ¿Quién interpreta los comodines: el comando (`ls`, `cp`...) o el shell? Teniendo eso en cuenta, ¿por qué en `find -name` hay que escribir el patrón entre comillas? Demuéstralo con un ejemplo en el que, sin comillas, `find` no haga lo que esperas.
