# 3.13 Permisos y propietarios

Cada fichero y cada directorio de Linux tiene un **propietario**, un **grupo** y unos **permisos** que deciden quién puede hacer qué con él. Es la base de la seguridad del sistema: es lo que impide que un alumno lea los exámenes del profesor o que un servicio comprometido modifique `/etc/shadow`.

## Leer los permisos

```bash
$ ls -l examen.odt
-rw-r----- 1 profe docentes 18240 oct 24 18:02 examen.odt
```

Los diez primeros caracteres se leen así:

| Posición | `-` | `rw-` | `r--` | `---` |
|---|---|---|---|---|
| Significado | Tipo | **Propietario** (u, *user*) | **Grupo** (g, *group*) | **Otros** (o, *others*) |

Es decir: `profe` puede leer y escribir; los miembros del grupo `docentes` solo leer; el resto, nada.

Para saber qué permisos se aplican a un usuario, el sistema comprueba **en este orden** y se queda con el **primero** que encaja:

1. ¿Es el propietario? → permisos de propietario.
2. ¿Pertenece al grupo? → permisos de grupo.
3. Si no → permisos de otros.

`root` se salta estas comprobaciones: puede leer y escribir cualquier fichero.

## Qué significa cada permiso

El mismo permiso tiene un significado distinto en ficheros y en directorios:

| Permiso | En un fichero | En un directorio |
|---|---|---|
| `r` (lectura) | Ver su contenido | **Listar** los nombres que contiene (`ls`) |
| `w` (escritura) | Modificar su contenido | **Crear, borrar y renombrar** ficheros dentro |
| `x` (ejecución) | Ejecutarlo como programa | **Entrar** en él (`cd`) y acceder a lo que contiene |

!!! warning "Borrar depende del directorio"
    Para borrar un fichero **no** hace falta permiso de escritura sobre el fichero, sino sobre el **directorio** que lo contiene. Por eso en `/tmp`, donde todos pueden escribir, hace falta el *sticky bit* (lo vemos en el apartado siguiente).

## Cambiar permisos: `chmod`

### Modo simbólico

```text
chmod  [quién][operación][permisos]  fichero
```

| Quién | Operación | Permisos |
|---|---|---|
| `u` propietario | `+` añadir | `r` |
| `g` grupo | `-` quitar | `w` |
| `o` otros | `=` establecer exactamente | `x` |
| `a` todos (u, g y o) | | |

```bash
$ chmod u+x script.sh            # el propietario puede ejecutarlo
$ chmod g-w informe.txt          # el grupo ya no puede escribir
$ chmod o= privado.txt           # otros: ningún permiso
$ chmod a+r publico.txt          # todos pueden leer
$ chmod u=rwx,g=rx,o= carpeta    # varios a la vez
$ chmod -R g+w proyecto/         # recursivo
```

### Modo octal

Cada permiso tiene un valor y se suman para cada grupo de tres:

| Permiso | Valor |
|---|---|
| `r` | 4 |
| `w` | 2 |
| `x` | 1 |

| Octal | Permisos | | Octal | Permisos |
|---|---|---|---|---|
| `7` | `rwx` | | `3` | `-wx` |
| `6` | `rw-` | | `2` | `-w-` |
| `5` | `r-x` | | `1` | `--x` |
| `4` | `r--` | | `0` | `---` |

Se escriben tres cifras: propietario, grupo y otros.

```bash
$ chmod 644 documento.txt     # rw-r--r--   (fichero normal)
$ chmod 600 clave_privada     # rw-------   (solo el propietario)
$ chmod 755 script.sh         # rwxr-xr-x   (programas y directorios)
$ chmod 750 carpeta           # rwxr-x---
$ chmod 700 ~/privado         # rwx------
```

!!! tip "¿Simbólico u octal?"
    El octal **establece todos los permisos de golpe**. El simbólico permite **cambiar solo uno** sin tocar el resto (`chmod g+w`), algo muy útil con `-R`.

## Cambiar propietario y grupo: `chown` y `chgrp`

Solo `root` puede cambiar el propietario. El propietario de un fichero puede cambiar su grupo, pero solo a uno de los grupos a los que él pertenece.

```bash
$ sudo chown ana informe.txt              # nuevo propietario
$ sudo chown ana:docentes informe.txt     # propietario y grupo
$ sudo chown :docentes informe.txt        # solo el grupo
$ sudo chown -R www-data:www-data /var/www/web   # recursivo
$ chgrp docentes informe.txt              # solo el grupo
$ chgrp -R docentes proyecto/
```

## Permisos por defecto: `umask`

Cuando se crea un fichero o un directorio, no se le dan todos los permisos: se parte de un máximo y se **quitan** los que indica la **`umask`**.

| | Máximo | `umask` habitual `022` | Resultado |
|---|---|---|---|
| Fichero | `666` (`rw-rw-rw-`) | quita `w` a grupo y otros | `644` (`rw-r--r--`) |
| Directorio | `777` (`rwxrwxrwx`) | quita `w` a grupo y otros | `755` (`rwxr-xr-x`) |

Los ficheros parten de `666` porque, por seguridad, nunca se crean con permiso de ejecución: hay que dárselo a propósito con `chmod`.

```bash
$ umask              # ver la máscara actual
0022
$ umask -S           # en forma simbólica
u=rwx,g=rx,o=rx
$ umask 027          # nuevos ficheros 640 y directorios 750
$ umask 077          # nuevos ficheros 600 y directorios 700 (máxima privacidad)
```

El cambio solo dura lo que la sesión; para que sea permanente se añade a `~/.bashrc` (para un usuario) o se configura en `/etc/login.defs` o `/etc/profile` (para todos).

## Permisos especiales

Además de `rwx` existen tres permisos especiales: **SUID**, **SGID** y ***sticky bit***. Los vemos a fondo en el apartado siguiente.

## Resumen

| Comando | Uso |
|---|---|
| `ls -l`, `ls -ld` | Ver permisos de ficheros / del propio directorio |
| `chmod` | Cambiar permisos (simbólico `u+x` u octal `755`) |
| `chown usuario:grupo` | Cambiar propietario y grupo |
| `chgrp` | Cambiar el grupo |
| `umask` | Ver o cambiar los permisos por defecto |
| `stat` | Ver los permisos en octal y otros metadatos |

## Ejercicios

**1.** Traduce a octal: `rwxr-x---`, `rw-rw-r--`, `r--------`, `rwxrwxrwx`.

??? success "Solución"
    `750`, `664`, `400`, `777`.

**2.** Traduce a letras: `640`, `711`, `555`, `604`.

??? success "Solución"
    `rw-r-----`, `rwx--x--x`, `r-xr-xr-x`, `rw----r--`.

**3.** Crea `notas.txt` y deja sus permisos en `rw-r-----` con modo simbólico y, después, con modo octal. Comprueba el resultado con `stat -c '%A %a' notas.txt`.

??? success "Solución"
    ```bash
    $ touch notas.txt
    $ chmod u=rw,g=r,o= notas.txt
    $ chmod 640 notas.txt
    $ stat -c '%A %a' notas.txt
    -rw-r----- 640
    ```

**4.** Crea un directorio `prueba` con un fichero dentro. Quítale el permiso `x` al directorio (`chmod u-x prueba`). ¿Puedes hacer `ls prueba`? ¿Y `cat prueba/fichero` o `cd prueba`? Ahora devuélvele la `x` y quítale la `r`. Repite las pruebas.

??? success "Solución"
    Sin `x`: `ls` muestra los nombres (con `ls -l` verás errores y `?` en lugar de los datos de cada fichero), pero no puedes entrar con `cd` ni leer los ficheros. Sin `r` (y con `x`): no puedes listar el contenido, pero sí entrar y leer `prueba/fichero` si conoces su nombre.

**5.** Escribe un script `hola.sh` que muestre `Hola`. Intenta ejecutarlo con `./hola.sh`. Dale permiso de ejecución solo al propietario y vuelve a probar.

??? success "Solución"
    ```bash
    $ echo 'echo Hola' > hola.sh
    $ ./hola.sh            # Permission denied
    $ chmod u+x hola.sh
    $ ./hola.sh
    ```

**6.** Con `umask 022`, ¿qué permisos tendrán un fichero y un directorio nuevos? ¿Y con `umask 077`? Compruébalo creando uno de cada.

??? success "Solución"
    Con `022`: fichero `644`, directorio `755`. Con `077`: fichero `600`, directorio `700`.
    ```bash
    $ umask 077
    $ touch f; mkdir d; ls -ld f d
    $ umask 022
    ```

**7.** Crea un fichero como tu usuario y cambia su propietario a `lucia` y su grupo a `asir1` con un solo comando. ¿Puedes hacerlo sin `sudo`?

??? success "Solución"
    ```bash
    $ touch entrega.txt
    $ sudo chown lucia:asir1 entrega.txt
    ```
    Sin `sudo` no: solo `root` puede cambiar el propietario de un fichero.
