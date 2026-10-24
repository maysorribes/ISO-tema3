# 3.3 Gestión básica de archivos

En Linux **todo es un fichero**: los documentos, los programas, los directorios e incluso los dispositivos. Por eso saber manejar ficheros desde la terminal es una de las destrezas básicas de cualquier administrador.

Un fichero tiene **contenido** y **metadatos** (tamaño, propietario, permisos, fechas). Los tipos que más usaremos son:

| Tipo | Símbolo en `ls -l` | Ejemplo |
|---|---|---|
| Fichero regular | `-` | `/etc/hostname` |
| Directorio | `d` | `/home` |
| Enlace simbólico | `l` | `/bin` en muchas distros |
| Dispositivo de caracteres | `c` | `/dev/tty1` |
| Dispositivo de bloques | `b` | `/dev/sda` |

## Rutas absolutas y relativas

- Una **ruta absoluta** empieza por `/` y se indica desde la raíz: `/home/alumno/Documentos/notas.txt`.
- Una **ruta relativa** parte del directorio actual: `Documentos/notas.txt`.

Atajos útiles:

| Atajo | Significado |
|---|---|
| `.` | Directorio actual |
| `..` | Directorio padre |
| `~` | Directorio personal del usuario |
| `-` | (con `cd`) directorio anterior |

```bash
$ pwd              # ¿dónde estoy?
$ cd /etc          # ruta absoluta
$ cd ..            # subo un nivel
$ cd ~/Documentos  # relativa a mi home
$ cd -             # vuelvo al directorio anterior
$ cd               # sin argumentos: vuelvo a mi home
```

## Listar: `ls`

```bash
$ ls                 # nombres
$ ls -l              # formato largo
$ ls -lh             # tamaños legibles (K, M, G)
$ ls -a              # incluye ocultos (empiezan por .)
$ ls -la /etc        # combinadas, sobre otro directorio
$ ls -lt             # ordenado por fecha de modificación
$ ls -lS             # ordenado por tamaño
$ ls -R              # recursivo: entra en los subdirectorios
$ ls -d */           # solo directorios
```

Cómo leer una línea de `ls -l`:

```text
-rw-r--r-- 1 alumno alumno 2048 oct 24 10:15 notas.txt
```

| Campo | Valor | Significado |
|---|---|---|
| 1.º carácter | `-` | Tipo (fichero regular) |
| Resto del 1.º campo | `rw-r--r--` | Permisos (propietario, grupo, otros) |
| 2.º | `1` | Número de enlaces |
| 3.º | `alumno` | Propietario |
| 4.º | `alumno` | Grupo |
| 5.º | `2048` | Tamaño en bytes |
| 6.º-8.º | `oct 24 10:15` | Fecha de última modificación |
| 9.º | `notas.txt` | Nombre |

## Crear ficheros: `touch`

`touch` crea ficheros vacíos (si no existen) o actualiza la fecha de los que ya existen:

```bash
$ touch practica.txt
$ touch a.txt b.txt c.txt      # varios a la vez
$ touch -m practica.txt        # actualiza solo la fecha de modificación
$ touch -a practica.txt        # actualiza solo la fecha de acceso
```

## Copiar: `cp`

```bash
cp [opciones] ORIGEN DESTINO
```

```bash
$ cp notas.txt copia.txt              # copia con otro nombre
$ cp notas.txt ~/Documentos/          # copia en otro directorio
$ cp a.txt b.txt c.txt ~/Documentos/  # varios ficheros a un directorio
$ cp -i notas.txt copia.txt           # pregunta antes de sobrescribir
$ cp -r proyecto/ copia_proyecto/     # copia un directorio entero
$ cp -p notas.txt copia.txt           # conserva permisos y fechas
```

!!! warning "`cp` sobrescribe sin avisar"
    Si el destino existe, `cp` lo reemplaza en silencio. Usa `-i` si no estás seguro.

## Mover y renombrar: `mv`

`mv` sirve para las dos cosas: mover a otro sitio y cambiar el nombre (en Linux, renombrar es "mover al mismo directorio con otro nombre").

```bash
$ mv notas.txt ~/Documentos/      # mueve
$ mv notas.txt apuntes.txt        # renombra
$ mv a.txt b.txt ~/Documentos/    # mueve varios
$ mv -i apuntes.txt viejo.txt     # pregunta si el destino existe
$ mv -f apuntes.txt viejo.txt     # fuerza sin preguntar
```

`mv` funciona con directorios **sin** necesidad de `-r`.

## Borrar ficheros: `rm`

```bash
$ rm basura.txt
$ rm a.txt b.txt c.txt
$ rm -i importante.txt        # pide confirmación
$ rm -f basura.txt            # fuerza, sin preguntar ni dar error si no existe
$ rm -r carpeta/              # borra un directorio y todo su contenido
$ rm -ri carpeta/             # recursivo pidiendo confirmación
```

!!! danger "No hay papelera"
    `rm` borra **definitivamente**. Mucho cuidado con `rm -rf` y con los comodines: un espacio de más en `rm -rf / tmp/*` (en lugar de `/tmp/*`) intentaría borrar el sistema entero.

## Directorios: `mkdir` y `rmdir`

```bash
$ mkdir practicas
$ mkdir uno dos tres                     # varios a la vez
$ mkdir -p ISO/tema3/ejercicios          # crea también los padres que falten
$ rmdir tres                             # solo si está vacío
$ rmdir -p ISO/tema3/ejercicios          # borra la cadena si todos quedan vacíos
```

`rmdir` falla si el directorio contiene algo; en ese caso hay que usar `rm -r`.

## Operaciones recursivas

Muchos comandos actúan sobre un directorio **y todo lo que hay dentro** con la opción `-r` (o `-R`, o `--recursive`):

| Comando | Sin recursividad | Con `-r` / `-R` |
|---|---|---|
| `ls` | Lista el directorio | `ls -R` lista también todos los subdirectorios |
| `cp` | Se niega a copiar directorios (`omitting directory`) | `cp -r` copia el árbol completo |
| `rm` | Se niega a borrar directorios (`Is a directory`) | `rm -r` borra el árbol completo |

El comando `tree` (puede que tengas que instalarlo con `sudo apt install tree`) muestra el árbol de forma gráfica.

## Comodines (*globbing*)

El shell permite referirse a varios ficheros a la vez con **comodines**. Es el shell quien los expande a la lista de nombres que coinciden **antes** de ejecutar el comando.

| Comodín | Coincide con | Ejemplo | Encaja con |
|---|---|---|---|
| `*` | Cualquier cadena (incluso vacía) | `*.txt` | `a.txt`, `notas.txt` |
| `?` | Exactamente un carácter | `tema?.md` | `tema1.md`, `temaA.md` |
| `[abc]` | Uno de los caracteres indicados | `tema[123].md` | `tema1.md`, `tema3.md` |
| `[a-z]` | Un carácter del rango | `[A-Z]*` | ficheros que empiezan por mayúscula |
| `[!abc]` | Un carácter que **no** esté en la lista | `[!0-9]*` | ficheros que no empiezan por dígito |

```bash
$ ls *.conf                     # todo lo que acaba en .conf
$ ls /etc/*.d                   # directorios de /etc acabados en .d
$ cp *.txt copias/              # copia todos los .txt
$ rm informe_??.pdf             # informe_01.pdf ... informe_99.pdf
$ ls examen[1-3].odt            # examen1, examen2, examen3
$ ls [abc]*                     # empiezan por a, b o c
$ mv *2025* archivo/            # contienen 2025 en cualquier posición
```

Los comodines se pueden combinar: `ls [st]?ma*` encaja con `tema3.md` y `sema.txt`.

!!! tip "Prueba antes de borrar"
    Antes de un `rm` con comodines, ejecuta el mismo patrón con `ls` para ver qué ficheros se verían afectados.

## Resumen de comandos

| Comando | Uso |
|---|---|
| `pwd` / `cd` | Ver / cambiar el directorio actual |
| `ls` | Listar |
| `touch` | Crear ficheros vacíos o actualizar fechas |
| `cp` | Copiar (`-r` para directorios) |
| `mv` | Mover o renombrar |
| `rm` | Borrar (`-r` para directorios) |
| `mkdir` | Crear directorios (`-p` para crear los padres) |
| `rmdir` | Borrar directorios vacíos |

## Ejercicios

**1.** Sin moverte de tu directorio personal, crea esta estructura con **un solo** comando `mkdir`:

```text
~/ISO/
└── tema3/
    ├── apuntes/
    └── practicas/
```

??? success "Solución"
    ```bash
    $ mkdir -p ISO/tema3/apuntes ISO/tema3/practicas
    ```
    O, usando la expansión de llaves de Bash: `mkdir -p ISO/tema3/{apuntes,practicas}`.

**2.** Dentro de `~/ISO/tema3/practicas` crea con un solo `touch` los ficheros `p1.txt`, `p2.txt`, `p3.txt`, `p10.txt`, `notas.md` y `Resumen.md`.

??? success "Solución"
    ```bash
    $ cd ~/ISO/tema3/practicas
    $ touch p1.txt p2.txt p3.txt p10.txt notas.md Resumen.md
    ```

**3.** Usando comodines, lista en ese directorio:

- a) Todos los `.txt`.
- b) Las prácticas de **una sola cifra** (`p1`, `p2`, `p3`).
- c) Las prácticas 1 y 3.
- d) Los ficheros que empiezan por mayúscula.

??? success "Solución"
    ```bash
    $ ls *.txt
    $ ls p?.txt
    $ ls p[13].txt
    $ ls [A-Z]*
    ```

**4.** Copia todos los `.md` a `~/ISO/tema3/apuntes`. Después **mueve** `p10.txt` a `apuntes` renombrándolo a `practica10.txt` en el mismo comando.

??? success "Solución"
    ```bash
    $ cp *.md ../apuntes/
    $ mv p10.txt ../apuntes/practica10.txt
    ```

**5.** Haz una copia de seguridad de todo `~/ISO/tema3` en `~/ISO/tema3.bak`. Comprueba el resultado con `ls -R`.

??? success "Solución"
    ```bash
    $ cp -r ~/ISO/tema3 ~/ISO/tema3.bak
    $ ls -R ~/ISO/tema3.bak
    ```

**6.** Intenta borrar `~/ISO/tema3.bak` con `rmdir`. ¿Qué pasa? Bórralo correctamente pidiendo confirmación de cada elemento.

??? success "Solución"
    `rmdir` da el error `Directory not empty` porque solo borra directorios vacíos.
    ```bash
    $ rm -ri ~/ISO/tema3.bak
    ```

**7.** En un directorio hay estos ficheros: `informe1.pdf`, `informe2.pdf`, `informe12.pdf`, `informe.pdf`, `informeA.pdf`. ¿Qué ficheros mostraría cada comando?

- a) `ls informe*.pdf`
- b) `ls informe?.pdf`
- c) `ls informe[0-9].pdf`
- d) `ls informe*[0-9].pdf`

??? success "Solución"
    - a) Todos.
    - b) `informe1.pdf`, `informe2.pdf`, `informeA.pdf`.
    - c) `informe1.pdf`, `informe2.pdf`.
    - d) `informe1.pdf`, `informe2.pdf`, `informe12.pdf`.

**8.** Interpreta los campos de esta línea de `ls -l`:

```text
drwxr-x--- 3 root adm 4096 oct 20 09:12 log
```

??? success "Solución"
    Es un **directorio** (`d`) llamado `log`, cuyo propietario es `root` y su grupo `adm`. El propietario puede leer, escribir y entrar (`rwx`); el grupo, leer y entrar (`r-x`); el resto, nada (`---`). Tiene 3 enlaces, ocupa 4096 bytes (el tamaño del propio directorio, no de su contenido) y se modificó el 20 de octubre a las 9:12.
