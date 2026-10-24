# Práctica 5 · Usuarios y grupos

[Descargar el enunciado en PDF](pdf/UT3_P5_Usuarios.pdf){ .md-button .md-button--primary }

| | |
|---|---|
| **Apartados de los apuntes** | 3.11 Gestión de usuarios y grupos · 3.12 Ficheros de cuentas |
| **Entorno** | Máquina virtual Ubuntu, con un usuario que pueda usar `sudo` |
| **Entrega** | `UT3_P5_Apellido_Nombre.pdf` |

## Resultados de aprendizaje y criterios de evaluación

Esta práctica contribuye a alcanzar el resultado de aprendizaje:

**RA2.** Configura el software de base, analizando las necesidades de explotación del sistema informático.

**CE2.1.** Se han planificado, creado y configurado cuentas de usuario, grupos, perfiles y políticas de contraseñas locales.

## Qué hay que entregar

Una memoria en PDF con, para cada ejercicio, el **comando** (como texto), una **captura** del resultado con tu *prompt* y la **respuesta razonada** a las preguntas. En cada ejercicio de creación o modificación, incluye también la **comprobación** (con `id`, `getent`, `chage -l`...).

!!! warning "No uses `adduser`"
    Resuelve los ejercicios con `useradd`, `usermod`, `groupadd`, etc., que son los comandos estándar en todas las distribuciones.

## Parte A · Crear usuarios y grupos

1. Crea el grupo `alumnos`. Crea el usuario `alumno1` con directorio personal y shell Bash, asígnale una contraseña y añádelo al grupo `alumnos` como grupo secundario.
2. Crea el grupo `progs`.
3. Crea el usuario `juan`, con directorio personal, shell Bash y `progs` como **grupo primario**.
4. Crea el grupo `externos`.
5. Crea el usuario `luis`, con `externos` como grupo primario y `progs` como grupo secundario.
6. Cambia la contraseña de `luis` a `SuJJh_4`.
7. Comprueba con `id` los grupos de los tres usuarios. ¿Por qué `juan` no tiene un grupo llamado `juan` y `alumno1` sí?

## Parte B · Plantillas y políticas de contraseñas

8. Haz que todos los usuarios que se creen **a partir de ahora** tengan en su directorio personal una carpeta `entregas` y un fichero `normas.txt` con el texto `Normas del aula de informática`. Crea el usuario `ana` y comprueba que los tiene. ¿Los tiene `juan`? ¿Por qué?
9. Asegúrate de que **todos** los usuarios cambian su contraseña cada **30 días** como máximo: tanto los que se creen a partir de ahora como los que ya existen (`alumno1`, `juan`, `luis` y `ana`).
10. Configura la cuenta de `ana` para que:

    a) Avise 5 días antes de que caduque la contraseña.
    b) Tenga que cambiar la contraseña la primera vez que entre.
    c) La cuenta expire el último día lectivo del curso.

    Entra como `ana` con `su - ana` y comprueba que te obliga a cambiar la contraseña.

## Parte C · Modificar y eliminar

11. Añade a `juan` al grupo `alumnos` **sin quitarle** de los grupos que ya tenga.
12. Cambia el comentario (nombre completo) de `luis` a `Luis García (externo)` y su shell a `/bin/sh`.
13. Haz que `juan` sea **administrador** del grupo `progs`. Entra como `juan` y añade a `alumno1` a ese grupo sin usar `sudo`.
14. Bloquea la cuenta de `luis`. Demuestra que no puede entrar y que se ve el bloqueo en `/etc/shadow`. Desbloquéala.
15. Elimina el usuario `ana` **con** su directorio personal y el usuario `alumno1` **sin** él. ¿Qué pasa con `/home/alumno1`? ¿De quién aparece ahora como propietario?
16. Intenta eliminar el grupo `externos`. ¿Por qué no puedes? ¿Qué tendrías que hacer antes?

## Parte D · Los ficheros de cuentas

17. Muestra las líneas de `juan` y `luis` en `/etc/passwd`, `/etc/shadow`, `/etc/group` y `/etc/gshadow`, y explica qué significa **cada campo**.
18. En `/etc/group`, el grupo `progs` muestra a `luis` como miembro pero no a `juan`. ¿Por qué, si los dos pertenecen al grupo?
19. Muestra con un solo comando los nombres de los usuarios **normales** del sistema (no las cuentas de servicio).
20. ¿Qué algoritmo usa tu sistema para cifrar las contraseñas? ¿Dónde se configura?

!!! question "Pregunta final"
    En un centro educativo con 300 alumnos, ¿qué ventajas tiene que las cuentas caduquen automáticamente al final de curso? ¿Qué diferencia hay entre caducar la **contraseña** y caducar la **cuenta**?
