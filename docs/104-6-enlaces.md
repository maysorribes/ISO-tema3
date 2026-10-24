# 3.15 Enlaces duros y simbólicos

Un **enlace** permite que un mismo fichero sea accesible desde **más de un nombre** o más de un sitio del sistema de archivos. Linux tiene dos tipos, que funcionan de forma muy distinta: los **enlaces duros** (o físicos) y los **enlaces simbólicos** (o blandos).

Para entenderlos hay que saber antes qué es un inodo.

## Inodos

En un sistema de archivos de Linux (ext4, xfs...), cada fichero se guarda en dos partes:

- El **inodo**: una estructura con un número único (dentro de ese sistema de archivos) que guarda los **metadatos** del fichero (tipo, permisos, propietario, tamaño, fechas) y **dónde están sus datos** en el disco. El inodo **no** guarda el nombre.
- Una **entrada de directorio**: es la que asocia un **nombre** a un número de inodo.

Un directorio, en realidad, no es más que una lista de pares *nombre → inodo*.

```bash
$ ls -i notas.txt            # número de inodo
1835123 notas.txt
$ ls -li                     # inodo y listado largo
$ stat notas.txt             # todos los metadatos del inodo
```

## Enlaces duros

Un enlace duro es **otro nombre** que apunta **al mismo inodo**. No hay "original" y "copia": los dos nombres son igual de válidos.

```bash
$ echo "Contenido" > original.txt
$ ln original.txt duro.txt
$ ls -li original.txt duro.txt
1835200 -rw-r--r-- 2 alumno alumno 10 oct 24 18:30 duro.txt
1835200 -rw-r--r-- 2 alumno alumno 10 oct 24 18:30 original.txt
```

Fíjate en:

- El **mismo número de inodo** (`1835200`) para los dos nombres.
- El **contador de enlaces** (la segunda columna) vale `2`: hay dos nombres apuntando a ese inodo.

Consecuencias:

- Si modificas uno, el cambio se ve en el otro: es **el mismo fichero**.
- Si borras uno, el otro sigue funcionando. `rm` solo quita un nombre y resta 1 al contador; los datos se liberan cuando el contador llega a **0**.
- Si mueves uno (dentro del mismo sistema de archivos), el otro no se entera: el inodo no cambia.

Limitaciones:

- **No** se pueden crear enlaces duros a **directorios** (salvo los `.` y `..` que crea el propio sistema).
- **No** pueden apuntar a otro **sistema de archivos** (otra partición, un USB...), porque los números de inodo solo son únicos dentro de cada uno.

!!! info "El contador de los directorios"
    Un directorio vacío tiene contador 2: su nombre en el directorio padre y su propio `.`. Cada subdirectorio que contiene le suma 1, por el `..` del hijo.

## Enlaces simbólicos

Un enlace simbólico es un **fichero especial** cuyo contenido es una **ruta** hacia otro fichero o directorio. Es parecido a un "acceso directo" de Windows.

```bash
$ ln -s original.txt simbolico.txt
$ ls -li original.txt simbolico.txt
1835200 -rw-r--r-- 1 alumno alumno 10 oct 24 18:30 original.txt
1835305 lrwxrwxrwx 1 alumno alumno 12 oct 24 18:31 simbolico.txt -> original.txt
```

Fíjate en:

- Tiene **su propio inodo** (`1835305`).
- El tipo es `l` y la flecha `->` muestra a dónde apunta.
- Su tamaño (12) es la longitud de la ruta que guarda (`original.txt`).
- Sus permisos siempre se ven como `rwxrwxrwx`, pero **no importan**: se aplican los del fichero de destino.

Ventajas frente a los duros:

- Pueden apuntar a **directorios**.
- Pueden apuntar a **otros sistemas de archivos**.

Inconvenientes:

- Si se borra, renombra o mueve el destino, el enlace queda **roto** (apunta a algo que no existe). `ls` suele mostrarlo en rojo.

### Rutas relativas o absolutas

La ruta que se guarda en el enlace se interpreta **desde el directorio donde está el enlace**, no desde donde estabas al crearlo:

```bash
$ cd ~
$ ln -s notas.txt Documentos/enlace     # ¡MAL! busca Documentos/notas.txt
$ ln -s ~/notas.txt Documentos/enlace   # bien: ruta absoluta
$ ln -s ../notas.txt Documentos/enlace  # bien: relativa al enlace
```

- Con **ruta absoluta**, el enlace sigue funcionando si lo mueves a otro sitio.
- Con **ruta relativa**, sigue funcionando si mueves **a la vez** el enlace y su destino (por ejemplo, al copiar un proyecto entero a otro lugar).

### Trabajar con enlaces simbólicos

```bash
$ readlink simbolico.txt             # a dónde apunta
$ readlink -f simbolico.txt          # ruta absoluta final (siguiendo todos los enlaces)
$ ln -sf nuevo.txt simbolico.txt     # -f: sustituye un enlace existente
$ rm simbolico.txt                   # borra el enlace, NO el destino
$ find . -xtype l                    # buscar enlaces rotos
```

!!! warning "Cuidado con la barra final"
    Con un enlace a un directorio, `rm enlace` borra el enlace, pero `rm -r enlace/` (con barra) puede borrar **el contenido del directorio de destino**.

## Comparativa

| | Enlace duro | Enlace simbólico |
|---|---|---|
| Comando | `ln destino nombre` | `ln -s destino nombre` |
| Inodo | El mismo que el destino | Uno propio |
| Contenido | Los mismos datos | Una ruta |
| A directorios | No | Sí |
| Entre sistemas de archivos | No | Sí |
| Si se borra el destino | Sigue funcionando | Queda roto |
| Tipo en `ls -l` | El del destino (`-`) | `l` |
| Permisos | Los del inodo (compartidos) | Los del destino |

## Dónde se usan

- **Enlaces simbólicos**: en todas partes. `/bin -> usr/bin` en las distribuciones modernas; las versiones de programas (`python3 -> python3.12`); los sitios activos de Apache y Nginx (`sites-enabled/` apunta a `sites-available/`); los servicios activos de systemd, en `/etc/systemd/system/`.
- **Enlaces duros**: menos visibles. Algunas herramientas de copia de seguridad (como `rsnapshot`) los usan para que los ficheros que no cambian entre copias no ocupen espacio de nuevo.

```bash
$ ls -l /bin /sbin /lib
$ ls -l /etc/alternatives | head
```

## Ejercicios

**1.** Crea `datos.txt` con algo de texto y un enlace duro `datos2.txt`. Comprueba con `ls -li` que comparten inodo y que el contador es 2. Modifica `datos2.txt` y comprueba que cambia `datos.txt`.

??? success "Solución"
    ```bash
    $ echo "linea 1" > datos.txt
    $ ln datos.txt datos2.txt
    $ ls -li datos*
    $ echo "linea 2" >> datos2.txt
    $ cat datos.txt
    ```

**2.** Borra `datos.txt`. ¿Qué pasa con `datos2.txt`? ¿Cuánto vale ahora el contador?

??? success "Solución"
    `datos2.txt` sigue existiendo con todo el contenido, y el contador vuelve a 1. Los datos solo se liberarán cuando se borre el último nombre.

**3.** ¿En qué se diferencia `ln datos2.txt copia_dura.txt` de `cp datos2.txt copia.txt`? Compruébalo con `ls -li` y modificando el original.

??? success "Solución"
    `ln` crea otro nombre para el **mismo inodo**: los cambios se ven en ambos. `cp` crea un **inodo nuevo** con una copia de los datos: a partir de ese momento son independientes.

**4.** Crea un enlace simbólico `atajo` en tu directorio personal que apunte a `/var/log`. Entra en él con `cd` y comprueba dónde estás con `pwd` y con `pwd -P`.

??? success "Solución"
    ```bash
    $ ln -s /var/log ~/atajo
    $ cd ~/atajo
    $ pwd          # /home/alumno/atajo  (ruta "lógica")
    $ pwd -P       # /var/log            (ruta física)
    ```

**5.** Crea `fichero.txt` y un enlace simbólico `enlace.txt` a él. Renombra `fichero.txt` a `otro.txt`. ¿Qué ocurre al hacer `cat enlace.txt`? ¿Cómo lo arreglas sin borrar el enlace a mano?

??? success "Solución"
    El enlace queda roto: `cat` responde `No such file or directory`.
    ```bash
    $ ln -sf otro.txt enlace.txt
    ```

**6.** Intenta crear un enlace duro a un directorio. ¿Qué mensaje da? ¿Y un enlace duro hacia un fichero de un USB o de `/dev/shm`?

??? success "Solución"
    ```bash
    $ ln /etc enlace_etc
    ln: /etc: hard link not allowed for directory
    $ touch /dev/shm/algo
    $ ln /dev/shm/algo ~/enlace
    ln: failed to create hard link ...: Invalid cross-device link
    ```
    Los enlaces duros no pueden apuntar a directorios ni a otros sistemas de archivos.

**7.** Desde tu directorio personal, crea en `~/Documentos` un enlace simbólico a `~/datos2.txt` usando primero una ruta relativa **incorrecta** y después una correcta. Usa `readlink -f` para comprobar a dónde apunta cada uno.

??? success "Solución"
    ```bash
    $ ln -s datos2.txt Documentos/mal         # apunta a Documentos/datos2.txt
    $ ln -s ../datos2.txt Documentos/bien
    $ readlink -f Documentos/mal Documentos/bien
    ```

**8.** Crea un directorio `vacio` y comprueba su contador de enlaces. Crea dentro dos subdirectorios y vuelve a mirarlo. Explica el resultado.

??? success "Solución"
    ```bash
    $ mkdir vacio; ls -ld vacio        # 2
    $ mkdir vacio/a vacio/b; ls -ld vacio   # 4
    ```
    2 por su nombre y su `.`, más 1 por cada subdirectorio, que contiene un `..` apuntando a él.

**9.** Busca los enlaces simbólicos que hay directamente en `/` y en `/etc/alternatives`. ¿A dónde apunta `/etc/alternatives/editor`?

??? success "Solución"
    ```bash
    $ find / -maxdepth 1 -type l -ls
    $ ls -l /etc/alternatives/editor
    $ readlink -f /etc/alternatives/editor
    ```

**10.** Encuentra los enlaces rotos de tu directorio personal y bórralos.

??? success "Solución"
    ```bash
    $ find ~ -xtype l
    $ find ~ -xtype l -delete
    ```
