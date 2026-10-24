# 3.4 Búsqueda, archivado y copia de archivos

Con el tiempo un sistema acumula miles de ficheros. En este apartado veremos cómo **encontrarlos** (`find`), cómo **agruparlos y comprimirlos** para hacer copias de seguridad o enviarlos (`tar`, `gzip`, `bzip2`, `cpio`) y cómo hacer **copias a bajo nivel** de ficheros y discos (`dd`).

## Buscar ficheros: `find`

```bash
find [DÓNDE] [CRITERIOS] [ACCIÓN]
```

- **Dónde**: directorio desde el que empieza a buscar (recorre también todos sus subdirectorios).
- **Criterios**: condiciones que deben cumplir los ficheros.
- **Acción**: qué hacer con lo encontrado (por defecto, mostrarlo).

### Por nombre

```bash
$ find . -name "notas.txt"
$ find ~ -name "*.pdf"            # todos los PDF de mi home
$ find /etc -iname "*.CONF"       # -iname ignora mayúsculas/minúsculas
$ find . -not -name "*.txt"       # los que NO acaban en .txt
```

!!! warning "Comillas con los comodines"
    Pon siempre el patrón entre comillas (`"*.pdf"`). Si no, el shell podría expandir el `*` con los ficheros del directorio actual antes de que `find` lo reciba, y la búsqueda no haría lo que esperas.

### Por tipo

| Opción | Busca |
|---|---|
| `-type f` | Ficheros regulares |
| `-type d` | Directorios |
| `-type l` | Enlaces simbólicos |

```bash
$ find ~ -type d -name "tema*"    # directorios que empiezan por "tema"
```

### Limitar la profundidad

```bash
$ find /etc -maxdepth 1 -name "*.conf"    # solo en /etc, sin entrar en subdirectorios
```

### Por tamaño

| Expresión | Significado |
|---|---|
| `-size 100c` | Exactamente 100 bytes |
| `-size +10k` | Más de 10 KiB |
| `-size -5M` | Menos de 5 MiB |
| `-size +1G` | Más de 1 GiB |
| `-empty` | Ficheros o directorios vacíos |

```bash
$ sudo find /var -size +100M
$ find ~ -size +10M -size -100M     # entre 10 y 100 MiB
$ find . -type f -empty
```

### Por fecha

| Expresión | Significado |
|---|---|
| `-mtime -7` | Modificados en los últimos 7 días |
| `-mtime +30` | Modificados hace más de 30 días |
| `-mmin -60` | Modificados en los últimos 60 minutos |

```bash
$ sudo find /etc -name "*.conf" -mtime -7
$ find /tmp -type f -mtime +30
```

!!! tip "`sudo` con `find /`"
    Buscar en directorios del sistema da muchos errores de `Permission denied`. Usa `sudo`, o descarta los errores con `2>/dev/null`.

### Acciones sobre los resultados

`-exec` ejecuta un comando por cada fichero encontrado. `{}` se sustituye por el nombre del fichero y la orden termina con `\;`:

```bash
$ find . -name "*.sh" -exec chmod +x {} \;          # da permiso de ejecución a los .sh
$ find . -type f -exec grep -l "ASIR" {} \;          # ficheros que contienen "ASIR"
$ find ~ -name "*.log" -exec ls -lh {} \;
```

`-delete` borra lo encontrado. **Comprueba siempre antes** sin `-delete`:

```bash
$ find . -name "*.bak"            # 1.º: miro qué saldría
$ find . -name "*.bak" -delete    # 2.º: borro
```

## Archivar: `tar`

`tar` (*tape archiver*) **agrupa** muchos ficheros y directorios en un único fichero (el "tarball"). Por sí solo **no comprime**, pero puede hacerlo a la vez usando gzip, bzip2 o xz.

```bash
tar OPERACIÓN[OPCIONES] -f FICHERO.tar [FICHEROS...]
```

### Operaciones

| Opción | Operación |
|---|---|
| `-c` | Crear un archivo |
| `-x` | Extraer |
| `-t` | Listar el contenido |

### Opciones habituales

| Opción | Efecto |
|---|---|
| `-f` | Nombre del fichero `.tar` (va justo antes del nombre) |
| `-v` | *Verbose*: muestra los ficheros que procesa |
| `-z` | Comprimir/descomprimir con gzip (`.tar.gz` o `.tgz`) |
| `-j` | Comprimir/descomprimir con bzip2 (`.tar.bz2`) |
| `-J` | Comprimir/descomprimir con xz (`.tar.xz`) |
| `-C dir` | Extraer en otro directorio |

### Ejemplos

```bash
$ tar -cvf tema3.tar ~/ISO/tema3            # crear
$ tar -tvf tema3.tar                        # ver qué contiene
$ tar -xvf tema3.tar                        # extraer en el directorio actual
$ tar -xvf tema3.tar -C /tmp                # extraer en /tmp

$ tar -czvf tema3.tar.gz ~/ISO/tema3        # crear comprimido con gzip
$ tar -xzvf tema3.tar.gz                    # extraer un .tar.gz
$ tar -cjvf tema3.tar.bz2 ~/ISO/tema3       # crear comprimido con bzip2
$ tar -cJvf tema3.tar.xz ~/ISO/tema3        # crear comprimido con xz
```

!!! tip "Regla mnemotécnica"
    **c**rear / e**x**traer / lis**t**ar + **z** (gzip) + **v** (ver) + **f** (fichero).
    Las versiones modernas de GNU tar detectan solas la compresión al extraer, así que `tar -xvf copia.tar.gz` también funciona.

## Comprimir ficheros sueltos: `gzip`, `bzip2`, `xz`

Estos comandos comprimen **un fichero** y, por defecto, **sustituyen el original** por la versión comprimida:

| Comprimir | Descomprimir | Extensión | Características |
|---|---|---|---|
| `gzip` | `gunzip` | `.gz` | Rápido, comprime algo menos |
| `bzip2` | `bunzip2` | `.bz2` | Más lento, comprime algo más |
| `xz` | `unxz` | `.xz` | El más lento, el que más comprime |

```bash
$ gzip informe.txt          # → informe.txt.gz (desaparece informe.txt)
$ gunzip informe.txt.gz     # → informe.txt
$ gzip -k informe.txt       # -k conserva el original
$ gzip -9 informe.txt       # máxima compresión (1 = rápida, 9 = máxima)
```

Para comprimir un **directorio** se combina con `tar`: primero se agrupa y luego se comprime, que es justo lo que hacen las opciones `-z`, `-j` y `-J`.

## `cpio`

`cpio` (*copy in, copy out*) también crea archivos, pero en lugar de recibir los nombres como argumentos, los **lee de la entrada estándar**, uno por línea. Por eso suele combinarse con `ls` o `find`:

```bash
$ ls | cpio -o > copia.cpio                  # -o: crear (copy out)
$ find ~/ISO -name "*.md" | cpio -o > md.cpio
$ cpio -id < copia.cpio                      # -i: extraer, -d: crear directorios
```

Es menos habitual que `tar` en el día a día, pero se usa, por ejemplo, en la imagen *initramfs* que carga el kernel al arrancar.

## Copias a bajo nivel: `dd`

`dd` copia datos **byte a byte**, sin importarle si son ficheros, particiones o discos enteros. Su sintaxis es distinta a la del resto de comandos: usa `opción=valor`.

| Opción | Significado |
|---|---|
| `if=` | Fichero o dispositivo de entrada (*input file*) |
| `of=` | Fichero o dispositivo de salida (*output file*) |
| `bs=` | Tamaño del bloque (p. ej. `bs=4M`) |
| `count=` | Número de bloques a copiar |
| `status=progress` | Muestra el progreso |
| `conv=ucase` | Convierte el texto a mayúsculas |

```bash
$ dd if=origen.txt of=copia.txt
$ dd if=origen.txt of=MAYUS.txt conv=ucase
$ dd if=/dev/zero of=relleno.img bs=1M count=100     # fichero de 100 MiB lleno de ceros
$ sudo dd if=/dev/sda of=disco.img bs=4M status=progress   # imagen de un disco entero
$ sudo dd if=ubuntu.iso of=/dev/sdb bs=4M status=progress  # grabar una ISO en un USB
```

!!! danger "Cuidado con `of=`"
    `dd` no pregunta nada. Si te equivocas de dispositivo en `of=` (por ejemplo `/dev/sda` en lugar de `/dev/sdb`) **sobrescribirás el disco del sistema**. Comprueba antes con `lsblk` qué dispositivo es cada uno.

## Resumen de comandos

| Comando | Uso |
|---|---|
| `find` | Buscar ficheros por nombre, tipo, tamaño o fecha, y actuar sobre ellos |
| `tar` | Agrupar ficheros en un archivo, opcionalmente comprimido |
| `gzip` / `gunzip` | Comprimir / descomprimir con gzip |
| `bzip2` / `bunzip2` | Comprimir / descomprimir con bzip2 |
| `xz` / `unxz` | Comprimir / descomprimir con xz |
| `cpio` | Crear y extraer archivos a partir de una lista de nombres |
| `dd` | Copiar datos byte a byte entre ficheros y dispositivos |

## Ejercicios

**1.** Busca en `/etc` todos los ficheros que acaban en `.conf`, **sin entrar en subdirectorios**. ¿Cuántos hay?

??? success "Solución"
    ```bash
    $ find /etc -maxdepth 1 -type f -name "*.conf" | wc -l
    ```

**2.** Busca en tu directorio personal todos los directorios llamados `tema` seguido de cualquier cosa, sin distinguir mayúsculas.

??? success "Solución"
    ```bash
    $ find ~ -type d -iname "tema*"
    ```

**3.** Busca en `/usr` los ficheros de más de 50 MiB. Evita que aparezcan los errores de permisos.

??? success "Solución"
    ```bash
    $ find /usr -type f -size +50M 2>/dev/null
    ```

**4.** Busca en tu home los ficheros modificados en las últimas 24 horas.

??? success "Solución"
    ```bash
    $ find ~ -type f -mtime -1
    ```
    O, con más precisión, `find ~ -type f -mmin -1440`.

**5.** Crea varios ficheros `.tmp` en un directorio de pruebas. Primero lístalos con `find` y después bórralos con el mismo `find`.

??? success "Solución"
    ```bash
    $ mkdir ~/pruebas && cd ~/pruebas
    $ touch a.tmp b.tmp c.tmp d.txt
    $ find . -name "*.tmp"
    $ find . -name "*.tmp" -delete
    ```

**6.** Con `find` y `-exec`, muestra con `ls -lh` los ficheros `.md` de `~/ISO`.

??? success "Solución"
    ```bash
    $ find ~/ISO -name "*.md" -exec ls -lh {} \;
    ```

**7.** Haz una copia de seguridad comprimida con gzip de `~/ISO` llamada `iso-AAAAMMDD.tar.gz` (con la fecha de hoy). Comprueba su contenido sin extraerlo.

??? success "Solución"
    ```bash
    $ tar -czvf iso-20261024.tar.gz ~/ISO
    $ tar -tzvf iso-20261024.tar.gz
    ```
    Para poner la fecha automáticamente: `tar -czvf iso-$(date +%Y%m%d).tar.gz ~/ISO`.

**8.** Extrae esa copia en `/tmp/restaurar` (crea antes el directorio).

??? success "Solución"
    ```bash
    $ mkdir /tmp/restaurar
    $ tar -xzvf iso-20261024.tar.gz -C /tmp/restaurar
    ```

**9.** Un compañero ejecuta `tar -cvf copia.tar.gz ~/documentos` pensando que ha comprimido la carpeta. ¿Qué ha hecho mal?

??? success "Solución"
    Le falta la opción `-z`. Ha creado un archivo `tar` **sin comprimir**, aunque lo haya llamado `.tar.gz`. Lo correcto es `tar -czvf copia.tar.gz ~/documentos`.

**10.** Comprime el mismo directorio con gzip, bzip2 y xz y compara los tamaños con `ls -lh`. ¿Cuál comprime más? ¿Cuál tarda más? (Usa `time` delante del comando para medirlo.)

??? success "Solución"
    ```bash
    $ time tar -czf prueba.tar.gz /usr/share/doc
    $ time tar -cjf prueba.tar.bz2 /usr/share/doc
    $ time tar -cJf prueba.tar.xz /usr/share/doc
    $ ls -lh prueba.tar.*
    ```
    Normalmente xz da el fichero más pequeño y tarda más; gzip es el más rápido y el que menos comprime.

**11.** Crea con `dd` un fichero de 20 MiB lleno de ceros y comprueba su tamaño. Después comprímelo con `gzip -k`. ¿Por qué se reduce tanto?

??? success "Solución"
    ```bash
    $ dd if=/dev/zero of=ceros.img bs=1M count=20
    $ ls -lh ceros.img
    $ gzip -k ceros.img
    $ ls -lh ceros.img*
    ```
    Un fichero formado solo por ceros es totalmente repetitivo, así que el algoritmo lo describe con muy poca información.
