# 3.10 Búsqueda y edición de texto con `grep` y `sed`

Ya conocemos lo básico de `grep` y `sed` (apartado 3.2) y sabemos escribir expresiones regulares (apartado 3.9). Ahora juntamos ambas cosas para buscar y transformar texto como lo hace un administrador: revisando logs, ficheros de configuración y salidas de comandos.

## `grep` a fondo

```bash
grep [opciones] PATRÓN [FICHEROS...]
```

| Opción | Efecto |
|---|---|
| `-i` | Ignora mayúsculas/minúsculas |
| `-v` | Invierte: líneas que **no** coinciden |
| `-c` | Cuenta las líneas que coinciden |
| `-n` | Muestra el número de línea |
| `-o` | Muestra solo la parte que coincide |
| `-w` | Solo palabras completas |
| `-x` | Solo si coincide la línea entera |
| `-l` | Solo el nombre de los ficheros que contienen coincidencias |
| `-H` / `-h` | Muestra / oculta el nombre del fichero en cada línea |
| `-r` | Busca recursivamente en un directorio |
| `-A N` / `-B N` / `-C N` | Muestra N líneas de contexto después / antes / alrededor |
| `-E` | Expresiones regulares extendidas (antes `egrep`) |
| `-F` | Patrón literal, sin expresiones regulares (antes `fgrep`) |
| `-f fichero` | Lee los patrones de un fichero (uno por línea) |
| `-e patrón` | Añade un patrón (se puede repetir) |
| `-z` | Las "líneas" terminan en carácter nulo (para usar con `find -print0`) |

### Ejemplos

```bash
$ grep -n 'PermitRootLogin' /etc/ssh/sshd_config     # ¿en qué línea está?
$ grep -Ev '^[[:space:]]*(#|$)' /etc/ssh/sshd_config  # configuración efectiva, sin comentarios ni vacías
$ grep -ri 'listen' /etc/nginx/                       # recursivo en un directorio
$ grep -rl 'ASIR' ~/ISO                               # qué ficheros lo contienen
$ grep -C 2 'error' /var/log/syslog                   # cada error con 2 líneas de contexto
$ grep -c 'Failed password' /var/log/auth.log         # intentos fallidos de SSH
$ grep -w 'root' /etc/passwd                          # "root" como palabra, no "chroot"
$ grep -e 'error' -e 'fail' -i /var/log/syslog        # varios patrones
$ grep -F '1.2.3.4' acceso.log                        # el punto es literal
```

!!! tip "Fichero de patrones"
    Con `-f` se busca una lista de cosas a la vez. Por ejemplo, si `bloqueadas.txt` tiene una IP por línea:
    ```bash
    $ grep -Ff bloqueadas.txt /var/log/nginx/access.log
    ```

### `grep` combinado con otros comandos

```bash
$ ps aux | grep -i ssh
$ ls -l /etc | grep -E '^l'                          # enlaces simbólicos de /etc
$ sudo fdisk -l | grep -E '^/dev/'                   # solo las particiones
$ find ~ -name '*.txt' -print0 | grep -z 'tema'      # filtrar nombres con -z
```

## `sed` a fondo

`sed` lee el texto **línea a línea**, le aplica las instrucciones y lo escribe en la salida estándar.

```bash
sed [opciones] 'DIRECCIÓN INSTRUCCIÓN' [FICHERO]
```

### Opciones

| Opción | Efecto |
|---|---|
| `-n` | No imprime nada salvo lo indicado con `p` |
| `-e` | Añade una instrucción (se puede repetir) |
| `-f fichero` | Lee las instrucciones de un fichero |
| `-E` o `-r` | Expresiones regulares extendidas |
| `-i[sufijo]` | Modifica el fichero original (con copia `fichero.sufijo` si se indica) |

### Direcciones: a qué líneas se aplica

Si no se indica dirección, la instrucción se aplica a **todas** las líneas.

| Dirección | Líneas |
|---|---|
| `5` | La línea 5 |
| `$` | La última |
| `3,8` | De la 3 a la 8 |
| `5,$` | De la 5 al final |
| `/patrón/` | Las que coinciden con el patrón |
| `/inicio/,/fin/` | Desde la que coincide con `inicio` hasta la que coincide con `fin` |
| `/patrón/!` | Las que **no** coinciden |

### Instrucciones

| Instrucción | Efecto |
|---|---|
| `p` | Imprimir la línea |
| `d` | Borrar la línea (de la salida) |
| `s/buscar/reemplazo/` | Sustituir |
| `a texto` | Añadir una línea **después** |
| `i texto` | Insertar una línea **antes** |
| `c texto` | Cambiar la línea por otra |
| `r fichero` | Insertar el contenido de un fichero después |
| `w fichero` | Escribir la línea en un fichero |
| `=` | Imprimir el número de línea |

```bash
$ sed -n '10,20p' /etc/passwd                     # líneas 10 a 20
$ sed '/^#/d; /^$/d' /etc/ssh/sshd_config         # sin comentarios ni vacías
$ sed -n '/^\[mysqld\]/,/^\[/p' /etc/mysql/my.cnf # una sección de un .ini
$ sed '1i # Fichero generado automáticamente' config.txt   # cabecera
$ sed '/^Port/a ListenAddress 0.0.0.0' sshd_config         # línea tras "Port"
$ sed '/^Port/c Port 2222' sshd_config                     # cambia la línea entera
$ sed -n '/ERROR/w errores.txt' app.log                    # guarda los errores aparte
$ sed -n '$=' fichero                                       # número de líneas (como wc -l)
```

### Sustituciones

```bash
s/BUSCAR/REEMPLAZO/MODIFICADORES
```

| Modificador | Efecto |
|---|---|
| `g` | Todas las apariciones de la línea (sin `g`, solo la primera) |
| `N` (un número) | Solo la aparición N |
| `i` | Ignorar mayúsculas/minúsculas |
| `p` | Imprimir la línea si hubo sustitución (útil con `-n`) |

```bash
$ sed 's/http:/https:/g' enlaces.txt
$ sed 's/,/;/2' datos.csv                 # solo la segunda coma de cada línea
$ sed -n 's/error/ERROR/gip' app.log      # muestra solo las líneas modificadas
$ sed -E 's/[[:space:]]+$//' fichero      # elimina espacios al final de línea
$ sed -E 's/^[[:space:]]+//' fichero      # elimina espacios al principio
```

Si el patrón contiene `/` (rutas), se puede usar **otro separador**:

```bash
$ sed 's|/home/alumno|/srv/datos|g' rutas.txt
```

En el reemplazo:

- `&` representa **todo** lo que ha coincidido.
- `\1`, `\2`... representan lo que coincidió con cada **grupo**.

```bash
$ echo "puerto 8080" | sed -E 's/[0-9]+/[&]/'
puerto [8080]
$ echo "Garcia, Ana" | sed -E 's/(.*), (.*)/\2 \1/'
Ana Garcia
$ echo "2026-10-24" | sed -E 's/([0-9]{4})-([0-9]{2})-([0-9]{2})/\3\/\2\/\1/'
24/10/2026
```

### Varias instrucciones

```bash
$ sed -e 's/a/A/g' -e 's/e/E/g' fichero
$ sed 's/a/A/g; s/e/E/g' fichero
```

O en un fichero de instrucciones:

```text title="limpiar.sed"
/^#/d
/^$/d
s/[[:space:]]+$//
```

```bash
$ sed -E -f limpiar.sed /etc/ssh/sshd_config
```

!!! warning "Antes de `-i`, prueba sin `-i`"
    Comprueba primero el resultado en pantalla. Cuando estés seguro, añade `-i.bak` para modificar el fichero conservando una copia.

## Combinando `grep` y `sed`: casos reales

**Usuarios que han iniciado sesión recientemente, sin repetir** (`last` muestra los inicios de sesión):

```bash
$ last | grep -Ev '^(reboot|wtmp|$)' | cut -d' ' -f1 | sort -u
```

**IPs que más veces han fallado al entrar por SSH:**

```bash
$ sudo grep 'Failed password' /var/log/auth.log \
    | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' \
    | sort | uniq -c | sort -nr | head
```

**Pasar un `ls -l` a CSV con nombre, propietario y tamaño:**

```bash
$ ls -l /etc | sed -E '1d; s/ +/ /g' | cut -d' ' -f3,5,9 | tr ' ' ','
```

**Sacar el valor de una directiva de configuración:**

```bash
$ grep -E '^[[:space:]]*Port' /etc/ssh/sshd_config | sed -E 's/^[[:space:]]*Port[[:space:]]+//'
```

## Resumen

| Herramienta | Para qué |
|---|---|
| `grep` | **Buscar**: seleccionar líneas que coinciden con un patrón |
| `grep -E` / `grep -F` | Patrones extendidos / literales |
| `grep -o`, `-c`, `-n`, `-l`, `-r`, `-C` | Partes, cuentas, números de línea, ficheros, recursivo, contexto |
| `sed -n '...p'` | Imprimir líneas o rangos |
| `sed '/.../d'` | Borrar líneas |
| `sed 's/.../.../g'` | Sustituir, con `&` y `\1` en el reemplazo |
| `sed 'a', 'i', 'c'` | Añadir, insertar, cambiar líneas |
| `sed -i.bak` | Modificar el fichero con copia de seguridad |

## Ejercicios

**1.** Muestra la configuración efectiva de `/etc/ssh/sshd_config`: sin comentarios ni líneas vacías. Hazlo con `grep` y después con `sed`.

??? success "Solución"
    ```bash
    $ grep -Ev '^[[:space:]]*(#|$)' /etc/ssh/sshd_config
    $ sed -E '/^[[:space:]]*(#|$)/d' /etc/ssh/sshd_config
    ```

**2.** Busca la palabra `localhost` en todos los ficheros de `/etc`, mostrando solo los nombres de los ficheros y sin errores de permisos.

??? success "Solución"
    ```bash
    $ grep -rlw localhost /etc 2>/dev/null
    ```

**3.** En `/var/log/syslog` (o `journalctl > log.txt` si no existe), muestra cada línea que contenga `error` (sin importar mayúsculas) con una línea de contexto antes y otra después, y con su número de línea.

??? success "Solución"
    ```bash
    $ sudo grep -in -C 1 'error' /var/log/syslog
    ```

**4.** Crea un fichero `ips.txt` con varias líneas que contengan IPs mezcladas con texto. Extrae solo las IPs, sin repetir y ordenadas.

??? success "Solución"
    ```bash
    $ grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' ips.txt | sort -u
    ```

**5.** Copia `/etc/passwd` a `mipasswd`. Con `sed`, cambia en la copia todos los shells `/bin/bash` por `/bin/zsh`. Usa otro separador para no tener que escapar las barras y guarda una copia de seguridad.

??? success "Solución"
    ```bash
    $ cp /etc/passwd mipasswd
    $ sed -i.bak 's|/bin/bash|/bin/zsh|' mipasswd
    $ diff mipasswd mipasswd.bak
    ```

**6.** Muestra las líneas 1, 5 y la última de `mipasswd` con una sola orden `sed`.

??? success "Solución"
    ```bash
    $ sed -n '1p; 5p; $p' mipasswd
    ```

**7.** Con `sed`, transforma las líneas de `mipasswd` en el formato `usuario -> home` (campos 1 y 6). Pista: grupos y `[^:]*`.

??? success "Solución"
    ```bash
    $ sed -E 's/^([^:]*):[^:]*:[^:]*:[^:]*:[^:]*:([^:]*):.*/\1 -> \2/' mipasswd
    ```

**8.** Tienes un fichero con fechas en formato `AAAA-MM-DD`. Pásalas todas a `DD/MM/AAAA`.

??? success "Solución"
    ```bash
    $ sed -E 's#([0-9]{4})-([0-9]{2})-([0-9]{2})#\3/\2/\1#g' fechas.txt
    ```
    Usar `#` como separador evita escapar las barras del reemplazo.

**9.** En un fichero `config.txt`, añade la línea `# Revisado por <tu usuario>` al principio y la línea `# Fin` al final.

??? success "Solución"
    ```bash
    $ sed -i -e "1i # Revisado por $USER" -e '$a # Fin' config.txt
    ```
    La primera instrucción va entre comillas dobles para que se expanda `$USER`; la segunda, entre simples para que el `$` de "última línea" no lo interprete el shell.

**10.** ¿Qué hace este comando? Pruébalo para comprobarlo.

```bash
$ sed -n '/^\[global\]/,/^\[/p' /etc/samba/smb.conf | grep -Ev '^[[:space:]]*([#;]|$)'
```

??? success "Solución"
    Muestra la sección `[global]` del fichero de Samba (desde la línea `[global]` hasta la siguiente cabecera de sección) y, de ella, solo las líneas que no son comentarios (`#` o `;`) ni están vacías. Es decir, la configuración global efectiva.

**11.** Muestra cuántos intentos fallidos de inicio de sesión por SSH ha habido en el sistema, y de qué IPs, de más a menos.

??? success "Solución"
    ```bash
    $ sudo grep -c 'Failed password' /var/log/auth.log
    $ sudo grep 'Failed password' /var/log/auth.log \
        | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' | sort | uniq -c | sort -nr
    ```
    En sistemas sin `/var/log/auth.log`, se puede usar `journalctl -u ssh` (o `-u sshd`) en lugar del fichero.
