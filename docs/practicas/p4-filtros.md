# Práctica 4 · Variables, filtros, tuberías y expresiones regulares

[Descargar el enunciado en PDF](pdf/UT3_P4_Filtros.pdf){ .md-button .md-button--primary }

| | |
|---|---|
| **Apartados de los apuntes** | 3.1 Variables · 3.2 Filtros de texto · 3.6 Tuberías · 3.9 Expresiones regulares · 3.10 `grep` y `sed` |
| **Entorno** | Máquina virtual Ubuntu |
| **Entrega** | `UT3_P4_Apellido_Nombre.pdf` |

## Objetivo

Extraer y transformar información de ficheros de texto y de la salida de otros comandos encadenando filtros con tuberías, y usar expresiones regulares con `grep` y `sed`.

## Qué hay que entregar

Una memoria en PDF con, para cada ejercicio, el **comando** (como texto), una **captura** del resultado con tu *prompt* y la **respuesta razonada** a las preguntas.

!!! warning "Una sola línea"
    Salvo que se diga lo contrario, cada ejercicio debe resolverse con **una sola línea** de comandos (puedes encadenar tantos como quieras con tuberías).

## Fichero de trabajo

Crea en `~/PRACTICA3` el fichero `equipos.txt` con este contenido. Es el inventario de los equipos de dos aulas (`nombre:ip:mac:sistema:ram_GB:aula`):

```text title="equipos.txt"
pc01:192.168.10.11:08:00:27:aa:01:11:Ubuntu 24.04:8:A101
pc02:192.168.10.12:08:00:27:aa:01:12:Windows 11:16:A101
pc03:192.168.10.13:08:00:27:aa:01:13:Ubuntu 24.04:8:A101
pc04:192.168.10.14:08:00:27:aa:01:14:Debian 12:4:A101
srv-web:192.168.10.2:08:00:27:bb:00:02:Debian 12:32:CPD
pc21:192.168.20.21:08:00:27:aa:02:21:Windows 11:16:A102
pc22:192.168.20.22:08:00:27:aa:02:22:Ubuntu 24.04:16:A102
pc23:192.168.20.23:08:00:27:aa:02:23:Windows 10:4:A102
pc24:192.168.20.24:08:00:27:aa:02:24:Ubuntu 22.04:8:A102
srv-dns:192.168.20.3:08:00:27:bb:00:03:Rocky Linux 9:16:CPD
```

!!! info "Ojo con el separador"
    La MAC también contiene `:`, así que cada línea tiene **más campos** de los que parece. Averigua en qué número de campo queda cada dato antes de usar `cut`.

## Parte A · Variables

1. Muestra el valor de las variables `HOME`, `USER`, `SHELL` y `PATH` con un solo `echo` que las presente con texto explicativo.
2. Crea la variable `AULA` con el valor `A101`. Abre un shell hijo (`bash`) y comprueba si existe. Sal, expórtala y repite la prueba. Explica lo que pasa.
3. Crea el directorio `~/bin`, añádelo al principio del `PATH` y crea dentro un script `inventario` que muestre el número de equipos de `equipos.txt`. Demuestra que puedes ejecutarlo escribiendo solo `inventario` desde cualquier directorio.

## Parte B · Ver ficheros

4. Muestra `/etc/passwd` con `cat`, con `less` y con `more`. ¿Qué diferencias hay?
5. Muestra las 3 primeras y las 2 últimas líneas de `equipos.txt`.
6. Muestra `equipos.txt` con las líneas numeradas.
7. ¿Cuántas líneas, palabras y caracteres tiene `equipos.txt`? ¿Por qué el número de palabras no coincide con el de líneas?

## Parte C · Filtros y tuberías

8. Muestra solo el nombre y la IP de cada equipo.
9. Muestra solo los equipos del aula `A102`.
10. ¿Cuántos equipos tienen algún Windows?
11. Muestra el nombre y la RAM de los equipos, ordenados de **más a menos** RAM.
12. ¿Cuántos equipos hay de cada sistema operativo? (Por ejemplo: `3 Ubuntu 24.04`.)
13. Muestra los sistemas operativos distintos que hay en el inventario, sin repetir y en orden alfabético.
14. Genera `equipos.csv`, con los mismos datos separados por `;` en lugar de `:`. ¿Qué problema da la MAC? ¿Cómo lo resolverías?
15. Muestra los nombres de los equipos en **mayúsculas**.
16. Usando `/etc/passwd`:

    a) ¿Cuántos usuarios tiene registrados el sistema?
    b) ¿Cuántos usan el intérprete `bash`?
    c) Muestra los nombres de usuario ordenados alfabéticamente y guárdalos en el fichero `usuarios`.
    d) Muestra el nombre de usuario y el shell de cada uno.

17. Muestra el listado de `/etc` con `ls -l`, pero solo con el **propietario**, el **tamaño** y el **nombre** de cada fichero. (Pista: los espacios repetidos de `ls -l` dan problemas a `cut`.)
18. Guarda en la variable `TOTAL` el número de equipos con Ubuntu (con sustitución de comandos) y muestra el mensaje `Hay N equipos con Ubuntu`.
19. Muestra el listado de `/etc` en pantalla y a la vez guárdalo en `etc.txt`, usando un solo comando con tubería.
20. Usando `find` y `xargs`, crea en `~/PRACTICA3/backup` una copia de todos los `.txt` de `~/PRACTICA3`.

## Parte D · Expresiones regulares con `grep` y `sed`

21. Muestra los equipos cuyo nombre empieza por `srv`.
22. Muestra los equipos cuya IP pertenece a la red `192.168.20.0/24`. (Cuidado: el punto en una expresión regular significa "cualquier carácter".)
23. Muestra los equipos que tienen **4 u 8** GB de RAM. Asegúrate de que la expresión no confunde `8` con el `8` de la MAC o de la IP.
24. Extrae **solo** las direcciones IP de todo el fichero (usa `grep -o`).
25. Muestra los equipos con Ubuntu **o** Debian usando una sola expresión regular extendida.
26. Con `sed`, muestra el fichero cambiando el aula `A101` por `Aula 101` (solo esa aula).
27. Con `sed`, muestra solo las líneas de la 3 a la 6.
28. Con `sed`, muestra el fichero sin las líneas de los servidores (`srv-`).
29. Con `sed` y grupos, transforma cada línea al formato `nombre -> ip` (solo esos dos datos).
30. Crea una copia de seguridad de `equipos.txt` y, con `sed -i`, actualiza **en el fichero** todos los `Ubuntu 22.04` a `Ubuntu 24.04`. Comprueba con `diff` el cambio.

## Parte E · Un caso real

31. Usando `/var/log/auth.log` (o `journalctl` si no existe), muestra **cuántas veces** se ha usado `sudo` en el sistema y **qué usuarios** lo han usado, sin repetir. (Pista: las líneas de `sudo` contienen `COMMAND=`.)

!!! question "Pregunta final"
    En el ejercicio 12, ¿por qué es imprescindible ordenar con `sort` antes de usar `uniq -c`? Demuéstralo con un ejemplo en el que, sin `sort`, el resultado sea incorrecto.
