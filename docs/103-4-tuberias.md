# 3.6 Tuberías, `tee`, sustitución de comandos y `xargs`

Las redirecciones conectan un programa con un **fichero**. Las tuberías conectan un programa con **otro programa**. Combinando ambas cosas se construyen órdenes muy potentes a partir de comandos sencillos.

## Tuberías: `|`

La barra vertical envía la **salida estándar** del comando de la izquierda a la **entrada estándar** del de la derecha. Se pueden encadenar tantos comandos como queramos:

```bash
$ cat /etc/passwd | wc -l
$ ls -l /etc | grep '^d' | wc -l              # ¿cuántos directorios hay en /etc?
$ cut -d: -f7 /etc/passwd | sort | uniq -c    # ¿qué shells usan los usuarios?
```

Los comandos de una tubería se ejecutan **a la vez**: cada uno va procesando los datos según le llegan, sin esperar a que el anterior termine.

### Las tuberías solo llevan `stdout`

Los errores **no** pasan por la tubería; siguen saliendo por pantalla:

```bash
$ ls /etc/hostname /nada | wc -l
ls: cannot access '/nada': No such file or directory
1
```

Para que también pasen, los unimos antes a `stdout`:

```bash
$ ls /etc/hostname /nada 2>&1 | wc -l
2
$ ls /etc/hostname /nada |& wc -l       # atajo de Bash equivalente
```

## Ver y guardar a la vez: `tee`

`tee` funciona como una "T" de fontanería: lee de la entrada estándar y lo escribe **a la vez** en la pantalla (o en la siguiente tubería) y en uno o varios ficheros.

```bash
$ ls -l /etc | tee listado.txt | wc -l        # guarda el listado y además cuenta líneas
$ ping -c 4 8.8.8.8 | tee ping.log            # lo veo y queda registrado
$ date | tee -a registro.log                  # -a: añade en vez de sobrescribir
```

!!! tip "`tee` y `sudo`"
    `sudo echo "texto" > /etc/fichero` **falla**, porque la redirección la hace tu shell (sin privilegios), no `sudo`. La forma correcta es:
    ```bash
    $ echo "192.168.1.10 servidor" | sudo tee -a /etc/hosts
    ```

## Sustitución de comandos: `$( )`

Permite usar la **salida de un comando** como parte de otro. El shell ejecuta lo que hay dentro de `$( )` y lo sustituye por su resultado:

```bash
$ echo "Hoy es $(date +%d/%m/%Y)"
Hoy es 24/10/2026
$ echo "Hay $(ls /etc | wc -l) elementos en /etc"
$ mkdir copia-$(date +%Y%m%d)
$ tar -czf home-$(whoami).tar.gz ~
```

También podemos guardar el resultado en una variable:

```bash
$ hoy=$(date +%Y-%m-%d)
$ sistema=$(uname -o)
$ echo "$sistema, $hoy"
GNU/Linux, 2026-10-24
```

!!! note "Comillas inversas"
    La forma antigua es `` `comando` `` (comillas inversas). Funciona igual, pero `$( )` se lee mejor y se puede anidar: `$(dirname $(which ls))`.

## Pasar la salida como argumentos: `xargs`

Hay comandos que **no leen de la entrada estándar**, sino que esperan los datos como **argumentos**. `rm`, `mkdir`, `cp` o `ls` son ejemplos: `echo fichero | rm` no hace nada útil.

`xargs` resuelve esto: lee de su entrada y construye con ello la línea de argumentos de otro comando.

```bash
$ echo "uno dos tres" | xargs mkdir         # equivale a: mkdir uno dos tres
$ find . -name "*.tmp" | xargs rm           # borra todos los .tmp encontrados
$ cat lista.txt | xargs ls -l
```

Opciones habituales:

| Opción | Efecto |
|---|---|
| `-n N` | Pasa como máximo N argumentos en cada ejecución |
| `-L N` | Pasa como máximo N **líneas** en cada ejecución |
| `-I {}` | Sustituye `{}` por cada elemento (se ejecuta una vez por elemento) |
| `-0` | Los elementos vienen separados por el carácter nulo (ver abajo) |
| `-p` | Pregunta antes de cada ejecución |

```bash
$ echo "a b c d" | xargs -n 2 echo
a b
c d
$ ls *.txt | xargs -I {} cp {} {}.bak       # copia cada .txt a .txt.bak
```

### Nombres con espacios: `-print0` y `-0`

`xargs` separa por espacios y saltos de línea, así que un fichero llamado `mis notas.txt` se convierte en dos argumentos (`mis` y `notas.txt`). La solución es que `find` separe los nombres con el carácter nulo (que no puede aparecer en un nombre de fichero) y que `xargs` lo sepa:

```bash
$ find . -name "*.txt" -print0 | xargs -0 rm
$ find . -type f -print0 | xargs -0 ls -lh
```

### `xargs` frente a `find -exec`

Hacen cosas parecidas. `-exec ... \;` lanza el comando **una vez por fichero**; `xargs` agrupa muchos ficheros en cada ejecución, por lo que suele ser más rápido con miles de ficheros. Con `find -exec comando {} +` (terminado en `+`) `find` también agrupa.

## Resumen

| Herramienta | Uso |
|---|---|
| `a | b` | La salida de `a` es la entrada de `b` |
| `a 2>&1 | b` o `a |& b` | Pasa también los errores por la tubería |
| `tee fichero` | Copia la entrada a un fichero y a la salida |
| `tee -a fichero` | Igual, pero añadiendo |
| `$(comando)` | Sustituye por la salida del comando |
| `xargs comando` | Convierte la entrada en argumentos de `comando` |

## Ejercicios

**1.** Muestra cuántos usuarios del sistema tienen como shell `/usr/sbin/nologin` (o `/sbin/nologin`), usando solo tuberías.

??? success "Solución"
    ```bash
    $ cut -d: -f7 /etc/passwd | grep nologin | wc -l
    ```

**2.** Lista los 5 ficheros o directorios que más ocupan dentro de `/var/log` (usa `du -s` y `sort`).

??? success "Solución"
    ```bash
    $ sudo du -s /var/log/* | sort -nr | head -n 5
    ```
    Con `du -sh` los tamaños son legibles, pero entonces hay que ordenar con `sort -hr`.

**3.** Ejecuta `ls -l /etc` de forma que veas el resultado en pantalla, se guarde en `etc.txt` y además se cuenten las líneas al final.

??? success "Solución"
    ```bash
    $ ls -l /etc | tee etc.txt | wc -l
    ```
    Con `| wc -l` al final, en pantalla solo se ve el número; el listado completo queda en `etc.txt`. Para ver ambos: `ls -l /etc | tee etc.txt` y luego `wc -l etc.txt`.

**4.** Añade la línea `127.0.1.1 aula` al final de `/etc/hosts` usando `echo` y `sudo` correctamente.

??? success "Solución"
    ```bash
    $ echo "127.0.1.1 aula" | sudo tee -a /etc/hosts
    ```

**5.** Guarda en la variable `fecha` la fecha de hoy con formato `AAAA-MM-DD` y crea un directorio `copia_<fecha>`.

??? success "Solución"
    ```bash
    $ fecha=$(date +%Y-%m-%d)
    $ mkdir copia_$fecha
    ```

**6.** Muestra el mensaje `El kernel es X y llevo Y usuarios en /etc/passwd`, donde X es la salida de `uname -r` e Y el número de líneas de `/etc/passwd`.

??? success "Solución"
    ```bash
    $ echo "El kernel es $(uname -r) y llevo $(wc -l < /etc/passwd) usuarios en /etc/passwd"
    ```

**7.** Crea en un directorio de pruebas los directorios `lunes`, `martes` y `miercoles` pasando sus nombres a `mkdir` mediante `xargs`.

??? success "Solución"
    ```bash
    $ echo "lunes martes miercoles" | xargs mkdir
    ```

**8.** Crea los ficheros `uno.log`, `dos.log` y `mi registro.log`. Bórralos todos con `find` y `xargs` sin que falle el que tiene un espacio.

??? success "Solución"
    ```bash
    $ touch uno.log dos.log "mi registro.log"
    $ find . -name "*.log" -print0 | xargs -0 rm
    ```

**9.** Para cada `.txt` del directorio actual, crea una copia con el sufijo `.bak` usando `xargs -I`.

??? success "Solución"
    ```bash
    $ ls *.txt | xargs -I {} cp {} {}.bak
    ```
