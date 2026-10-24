# Práctica 1 · Archivos y directorios

[Descargar el enunciado en PDF](pdf/UT3_P1_Archivos.pdf){ .md-button .md-button--primary }

| | |
|---|---|
| **Apartados de los apuntes** | 3.3 Gestión básica de archivos · 3.4 Búsqueda, archivado y copia |
| **Entorno** | Máquina virtual Ubuntu instalada en el Tema 1 |
| **Entrega** | `UT3_P1_Apellido_Nombre.pdf` |

## Objetivo

Moverse con soltura por el árbol de directorios usando rutas absolutas y relativas, y crear, copiar, mover, renombrar, borrar y empaquetar ficheros y directorios desde la terminal.

## Qué hay que entregar

Una memoria en PDF en la que, para **cada ejercicio**, aparezca:

1. El **comando** o comandos utilizados (como texto, no solo en la captura).
2. Una **captura** donde se vea el resultado y el *prompt* con tu usuario.
3. La **respuesta razonada** cuando el ejercicio haga una pregunta.

!!! warning "Trabaja siempre dentro de tu directorio personal"
    Salvo que el enunciado diga lo contrario, todo se crea dentro de `~/PRACTICA1`. No borres nada fuera de él.

## Parte A · Rutas y navegación

1. Muestra en qué directorio estás al abrir la terminal. ¿Qué ruta absoluta tiene tu directorio personal?
2. Crea en tu directorio personal el directorio `PRACTICA1`.
3. Dentro de `PRACTICA1` crea los directorios `PRUEBA1` y `PRUEBA2`, y dentro de este último `PRUEBA2.1`, **con una sola orden**. Comprueba el resultado con `tree` o con `ls -R`.
4. Sitúate en `PRUEBA2.1` y comprueba dónde estás.
5. Sitúate en el directorio raíz. Vuelve al directorio anterior **sin escribir su ruta**.
6. Vuelve a tu directorio personal con la orden más corta posible.
7. Desde tu directorio personal, sin moverte, muestra el contenido del directorio raíz. Después muéstralo con información detallada de cada elemento.
8. Estando en tu directorio personal, ¿son equivalentes estas tres órdenes? Razónalo y compruébalo.

    ```text
    cd /etc
    cd ../../etc
    cd
    ```

9. Elimina `PRUEBA2.1` sin salir de tu directorio personal.

## Parte B · Crear estructuras

10. Crea dentro de `PRACTICA1` esta estructura usando el menor número posible de órdenes:

    ```text
    PRACTICA1
    ├── COPIAS
    ├── MODELOS
    │   ├── IMPRESOS
    │   ├── INFORMES
    │   └── INSTANCIAS
    ├── TEMPORAL
    └── TRABAJOS
        └── TEXTOS
    ```

11. Intenta crear en `COPIAS` dos directorios con el mismo nombre `INF`. ¿Es posible? Después crea `Inf` e `InF`. ¿Es posible? ¿Por qué?
12. Sitúate en `INFORMES`. Indica **sin ejecutarlas** a qué directorio te llevaría cada una de estas órdenes (suponiendo que vuelves a `INFORMES` después de cada una) y después compruébalo:

    ```text
    cd ..
    cd ../../
    cd ../IMPRESOS
    cd ../../TEXTOS
    ```

13. Escribe una orden con **ruta absoluta** y otra con **ruta relativa** para pasar de `IMPRESOS` a `INSTANCIAS`.
14. Ejecuta `mkdir carpeta de trabajo` y `mkdir "carpeta de trabajo"` dentro de `TEMPORAL`. ¿Qué diferencia hay? Deja solo el directorio con espacios.
15. Crea el directorio oculto `.INVISIBLE` dentro de `PRACTICA1`. Comprueba que `ls` no lo muestra y averigua cómo verlo.

## Parte C · Copiar, mover y borrar

16. Copia el fichero `/etc/os-release` a `PRACTICA1/TRABAJOS/TEXTOS` con el nombre `sistema.txt`. Muestra su contenido.
17. Copia `sistema.txt` a `COPIAS`, `IMPRESOS` e `INFORMES`. Después comprueba con **un solo comando** `ls` que está en los tres sitios.
18. Copia el fichero `/etc/passwd` a `TEMPORAL` y cámbiale el nombre a `listado_usuarios.txt`.
19. Copia a `COPIAS` todos los ficheros de `/etc` que acaben en `.conf`. ¿Por qué no hace falta `sudo`? ¿Aparece algún error? ¿Por qué?
20. Copia el directorio `/etc/apt` **completo** (con sus subdirectorios) dentro de `COPIAS`.
21. Mueve el directorio `TEXTOS` y todo su contenido dentro de `MODELOS`.
22. Cambia el nombre de `TEMPORAL` a `TMP_PRACTICA`.
23. Oculta el fichero `sistema.txt` que hay dentro de `INFORMES` (sin borrarlo).
24. Crea en `TMP_PRACTICA` los directorios `dira`, `dirb`, `dirc` y `dird` con una sola orden, y después bórralos todos **excepto** `dira` con una sola orden.
25. Copia el directorio personal de otro usuario del sistema (si no hay ninguno, usa `/etc/skel`) dentro de `COPIAS`, incluido el propio directorio. ¿Puedes copiar todo? ¿Por qué?
26. Borra el directorio `COPIAS` con todo su contenido pidiendo confirmación de cada elemento. Cancela a mitad (++ctrl+c++) y después bórralo sin confirmación.

## Parte D · Empaquetar y comprimir

27. Empaqueta (sin comprimir) el directorio `PRACTICA1` en el fichero `~/copia.tar`.
28. Empaquétalo y comprímelo con gzip en `~/copia.tar.gz`, y con bzip2 en `~/copia.tar.bz2`.
29. Compara el tamaño de los tres ficheros con `ls -lh`. ¿Cuál ocupa menos? ¿Por qué el `.tar` ocupa más o menos lo mismo que la carpeta original?
30. Muestra el contenido de `copia.tar.gz` **sin extraerlo**.
31. Crea el directorio `/tmp/restaurar_TUUSUARIO` y extrae en él `copia.tar.gz`. Comprueba que la estructura está completa.
32. Borra `/tmp/restaurar_TUUSUARIO` y los tres ficheros de copia.

!!! question "Pregunta final"
    Explica con tus palabras la diferencia entre **empaquetar** y **comprimir**, y por qué con `tar` se hacen normalmente las dos cosas a la vez.
