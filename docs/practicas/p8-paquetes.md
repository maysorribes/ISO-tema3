# Práctica 8 · Administración de paquetes en Debian y Red Hat

[Descargar el enunciado en PDF](pdf/UT3_P8_Paquetes.pdf){ .md-button .md-button--primary }

| | |
|---|---|
| **Material de lectura** | LPI 102.4 [Gestión de paquetes Debian](https://learning.lpi.org/es/learning-materials/101-500/102/102.4/102.4_01/) · LPI 102.5 [Gestión de paquetes RPM y YUM](https://learning.lpi.org/es/learning-materials/101-500/102/102.5/) |
| **Entorno** | Máquina virtual Ubuntu y máquina virtual Fedora |
| **Entrega** | `UT3_P8_Apellido_Nombre.pdf` |

## Objetivo

Instalar, consultar y eliminar software con las herramientas de bajo nivel (`dpkg`, `rpm`) y de alto nivel (`apt`, `dnf`) de las dos grandes familias de distribuciones.

## Qué hay que entregar

Una memoria en PDF con las **respuestas** a las preguntas y, para cada ejercicio, los **comandos** (como texto) y una **captura de todo el proceso**, en la que se vea el *prompt* con tu usuario.

## Parte A · Debian y derivadas (Ubuntu)

Las distribuciones de la familia Debian usan paquetes `.deb`. La herramienta de más bajo nivel es `dpkg`; por encima está `apt` (sucesora de `apt-get`), que facilita mucho la tarea.

**Preguntas:**

- ¿Cuál es la principal ventaja de usar `apt` frente a `dpkg`?
- ¿Qué diferencias hay entre `apt` y `apt-get`?
- ¿Qué contiene el fichero `/etc/apt/sources.list` (o los ficheros de `/etc/apt/sources.list.d/`)?

**Ejercicios** (en Ubuntu):

1. Actualiza la lista de paquetes disponibles y muestra cuántos paquetes se pueden actualizar.
2. Busca con `apt` un paquete que sirva para mostrar el árbol de directorios y muestra su información (versión, tamaño, dependencias).
3. Descarga el fichero `.deb` de ese paquete **sin instalarlo** e instálalo con `dpkg`.
4. Comprueba con `dpkg` que está instalado y muestra la lista de ficheros que ha instalado. ¿Dónde ha quedado el ejecutable?
5. Elimina el paquete con `dpkg`.
6. Instala con `apt` un paquete que tenga **dependencias** (por ejemplo, `cowsay` o `htop`). ¿Qué paquetes adicionales se instalan?
7. Elimina el paquete con `apt`. ¿Qué diferencia hay entre `apt remove` y `apt purge`? ¿Y qué hace `apt autoremove`?

## Parte B · Red Hat y derivadas (Fedora)

Las distribuciones de la familia Red Hat usan paquetes `.rpm`. La herramienta de más bajo nivel es `rpm`; por encima está `dnf` (sucesora de `yum`).

**Preguntas:**

- ¿Cuál es la principal ventaja de usar `dnf` frente a `rpm`?
- ¿Qué diferencias hay entre `dnf` y `yum`?
- ¿Dónde se configuran los repositorios en Fedora?

**Ejercicios** (en Fedora):

8. Busca con `dnf` el mismo tipo de paquete que en el ejercicio 2 y muestra su información.
9. Descarga el `.rpm` sin instalarlo e instálalo con `rpm`.
10. Comprueba con `rpm` que está instalado y muestra los ficheros que ha instalado.
11. Elimina el paquete con `rpm`.
12. Instala con `dnf` un paquete que tenga dependencias y elimínalo después. Muestra el historial de operaciones de `dnf`.

## Parte C · Comparativa

13. Completa esta tabla con el comando equivalente en cada sistema:

    | Tarea | Ubuntu (`apt` / `dpkg`) | Fedora (`dnf` / `rpm`) |
    |---|---|---|
    | Actualizar la lista de paquetes | | |
    | Actualizar todo el sistema | | |
    | Buscar un paquete | | |
    | Ver información de un paquete | | |
    | Instalar un paquete del repositorio | | |
    | Instalar un fichero de paquete descargado | | |
    | Listar los paquetes instalados | | |
    | Ver qué ficheros instaló un paquete | | |
    | Saber a qué paquete pertenece un fichero | | |
    | Eliminar un paquete | | |

!!! question "Pregunta final"
    ¿Por qué es más seguro instalar software desde los repositorios oficiales de la distribución que descargando paquetes sueltos de una página web?
