# Práctica 6 · Permisos

[Descargar el enunciado en PDF](pdf/UT3_P6_Permisos.pdf){ .md-button .md-button--primary }

| | |
|---|---|
| **Apartados de los apuntes** | 3.13 Permisos y propietarios · 3.14 Permisos especiales |
| **Entorno** | Máquina virtual Ubuntu, con un usuario que pueda usar `sudo` |
| **Entrega** | `UT3_P6_Apellido_Nombre.pdf` |

## Resultados de aprendizaje y criterios de evaluación

Esta práctica contribuye a alcanzar el resultado de aprendizaje:

**RA2.** Configura el software de base, analizando las necesidades de explotación del sistema informático.

**CE2.1.** Se han planificado, creado y configurado cuentas de usuario, grupos, perfiles y políticas de contraseñas locales.

## Qué hay que entregar

Una memoria en PDF con, para cada ejercicio, el **comando** (como texto), una **captura** del resultado con tu *prompt* y la **respuesta razonada** a las preguntas.

!!! warning "Dos formas"
    Todos los cambios de permisos con `chmod` debes resolverlos de **dos maneras**: en modo **numérico** (octal) y en modo **simbólico** (letras).

## Parte A · Preparación

1. Crea los grupos `oficina1` y `oficina2`.
2. Crea los usuarios `pedro` y `pablo`, con directorio personal y shell Bash, que pertenezcan **únicamente** al grupo `oficina1`.
3. Crea los usuarios `alba` y `nerea`, que pertenezcan **únicamente** al grupo `oficina2`.

## Parte B · Permisos básicos

4. Como `pedro`, crea el fichero `secret.txt` al que **solo él** tenga acceso, de lectura y escritura.
5. Como `pedro`, crea el fichero `ventas_trimestre.txt` que puedan leer y modificar todos los usuarios de **su grupo**. Comprueba como `pablo` que puedes modificarlo. ¿Qué permisos necesita además el directorio personal de `pedro` para que `pablo` pueda llegar al fichero?
6. Como `alba`, crea el fichero `empleados.txt` que pueda **leer cualquier usuario**, y leer y modificar cualquiera de **su grupo**.
7. Copia `empleados.txt` a tu directorio personal y haz que su propietario y su grupo sean **tu usuario**.
8. Crea el usuario `modesto`, perteneciente a `oficina2`. Dentro de su directorio personal crea el directorio `compartido_con_todos`.
9. Dentro de ese directorio crea los ficheros `telefono_contactos`, `gastos_marzo` y `sueldos`, y escribe varias líneas en cada uno.
10. Da permiso de **lectura** a `compartido_con_todos` y a todos los ficheros que contiene para **todos** los usuarios. ¿Basta con la `r` para que los demás puedan leer los ficheros? Compruébalo como `pedro` y corrígelo si hace falta.
11. Restringe la escritura de `telefono_contactos` para que solo lo puedan modificar los usuarios del **grupo** de su propietario.
12. Cambia los permisos de `gastos_marzo` para que solo pueda modificarlo su propietario y **leerlo** cualquiera de su grupo.
13. Cambia los permisos de `sueldos` para que **solo su dueño** pueda leerlo y modificarlo.
14. Si un usuario tiene permiso de lectura sobre un fichero, pero el fichero está dentro de un directorio sobre el que **no tiene permiso de lectura**, ¿podrá leer el fichero? ¿Y si lo que le falta es el permiso de **ejecución** del directorio? Haz las dos pruebas y explica los resultados.

## Parte C · Interpretar permisos

15. Ejecutamos `ls -al` y obtenemos este resultado:

    ```text
    drwxr-xr-x   3 carles finances 4096 17 ene 16:05 .
    drwxr-xr-x 214 carles finances 4096  4 ene 19:37 ..
    -rwxr-sr-t   1 carles finances   34  6 jul 16:54 dadespersonals
    dr-xrwxr--   2 carles produccio 4096  6 jul 16:55 magatzem
    ```

    En `/etc/passwd` aparecen estas líneas:

    ```text
    carles:x:700:705::/home/carles:/bin/bash
    carlota:x:701:706::/home/carlota:/bin/bash
    maria:x:702:705::/home/maria:/bin/bash
    gregori:x:703:707::/home/gregori:/bin/bash
    ```

    Y en `/etc/group`:

    ```text
    finances:x:705:carlota
    produccio:x:706:carles
    menjador:x:707:
    ```

    Contesta **justificando** cada respuesta:

    a) ¿Puede `gregori` editar el archivo `dadespersonals`?
    b) ¿Puede `carles` editar el archivo `dadespersonals`?
    c) ¿Puede `maria` leer `dadespersonals`?
    d) ¿Puede `carles` entrar (`cd`) en el directorio `magatzem`?
    e) ¿Puede `carlota` entrar en el directorio `magatzem`?
    f) ¿Puede `carles` borrar o añadir archivos en `magatzem`?
    g) ¿Qué permisos especiales tiene `dadespersonals`? ¿Tienen algún efecto?

## Parte D · Permisos por defecto y permisos especiales

16. Muestra tu `umask` en octal y en modo simbólico. Calcula qué permisos tendrán un fichero y un directorio nuevos, y compruébalo.
17. Cambia la `umask` para que los ficheros nuevos **solo los pueda leer y escribir su propietario** y los directorios nuevos solo los pueda usar él. Comprueba el resultado y explica cómo harías el cambio permanente para tu usuario.
18. Crea el directorio `/srv/oficina1`, de manera que:

    a) Todos los miembros de `oficina1` puedan crear ficheros en él.
    b) Los ficheros nuevos pertenezcan automáticamente al grupo `oficina1`.
    c) Ningún miembro pueda borrar los ficheros de otro.
    d) El resto de usuarios no pueda ni entrar.

    Demuestra cada uno de los cuatro puntos con `pedro`, `pablo` y `alba`.

19. Busca en el sistema todos los ficheros con SUID y elige **tres**. Explica para qué sirve cada uno y por qué necesita ese permiso.

!!! question "Pregunta final"
    ¿Por qué `/tmp` tiene permisos `rwxrwxrwt`? ¿Qué podría pasar si se le quitara el *sticky bit*?
