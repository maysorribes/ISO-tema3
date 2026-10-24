# 3.14 Permisos especiales: SUID, SGID y *sticky bit*

Los permisos `rwx` del apartado anterior cubren la mayoría de situaciones, pero no todas:

- ¿Cómo puede un usuario normal cambiar su contraseña si `/etc/shadow` solo lo puede modificar `root`?
- ¿Cómo conseguimos que en una carpeta compartida los ficheros nuevos sean del grupo del departamento?
- ¿Cómo evitamos que en `/tmp`, donde todos pueden escribir, un usuario borre los ficheros de otro?

Para eso existen tres **permisos especiales**.

## SUID (*Set User ID*)

Un **programa** con SUID se ejecuta con los permisos de su **propietario**, no con los de quien lo lanza.

```bash
$ ls -l /usr/bin/passwd
-rwsr-xr-x 1 root root 68208 ... /usr/bin/passwd
```

La `s` en el lugar de la `x` del propietario indica el SUID. Como el propietario es `root`, cuando cualquier usuario ejecuta `passwd`, el programa funciona como si lo hubiera lanzado `root`, y por eso puede modificar `/etc/shadow`. El propio programa se encarga de que cada usuario solo pueda cambiar **su** contraseña.

- Solo tiene efecto en **ficheros ejecutables**.
- **No tiene efecto en directorios.**
- **No funciona en scripts** de Bash: Linux lo ignora por seguridad. Si un script necesita privilegios, se usa `sudo`.

Otros programas con SUID habituales: `sudo`, `su`, `mount`, `umount`, `chsh`.

## SGID (*Set Group ID*)

### En directorios

Es el uso más frecuente. Los ficheros que se crean dentro **heredan el grupo del directorio**, en lugar del grupo primario de quien los crea.

```bash
$ ls -ld /srv/proyecto
drwxrwsr-x 2 root informatica 4096 ... /srv/proyecto
$ touch /srv/proyecto/nuevo.txt       # lo crea ana, cuyo grupo primario es "ana"
$ ls -l /srv/proyecto/nuevo.txt
-rw-r--r-- 1 ana informatica 0 ... nuevo.txt   ← hereda el grupo informatica
```

Sin SGID, cada fichero quedaría con el grupo personal de su autor y los compañeros no podrían trabajar con él.

### En ficheros ejecutables

Igual que el SUID, pero con el **grupo**: el programa se ejecuta con los permisos del grupo propietario del fichero. Por ejemplo, `/usr/bin/crontab` tiene SGID del grupo `crontab`.

## *Sticky bit*

Se usa en **directorios**: solo el **propietario de cada fichero** (o `root`) puede **borrarlo o renombrarlo**, aunque los demás tengan permiso de escritura en el directorio.

```bash
$ ls -ld /tmp
drwxrwxrwt 18 root root 4096 ... /tmp
```

La `t` en el lugar de la `x` de otros indica el *sticky bit*. Todos pueden crear ficheros en `/tmp`, pero nadie puede borrar los de otro. Recuerda que, sin este bit, el permiso de escritura en un directorio permite borrar **cualquier** fichero que contenga.

En ficheros no tiene efecto en Linux.

## Cómo se ven

Los tres aparecen **en el lugar de la `x`** que les corresponde:

| Permiso | Dónde aparece | Con `x` debajo | Sin `x` debajo |
|---|---|---|---|
| SUID | Propietario | `rws` | `rwS` |
| SGID | Grupo | `r-s` | `r-S` |
| *Sticky* | Otros | `rwt` | `rwT` |

La **mayúscula** indica que el permiso especial está puesto pero falta la `x`.

## Cómo se asignan

### En modo simbólico

```bash
$ chmod u+s programa          # SUID
$ chmod g+s /srv/proyecto     # SGID
$ chmod +t /srv/compartida    # sticky bit
$ chmod u-s programa          # quitar el SUID
```

### En octal

Se añade una **cuarta cifra a la izquierda**, sumando:

| Valor | Permiso |
|---|---|
| `4` | SUID |
| `2` | SGID |
| `1` | *Sticky bit* |

```bash
$ chmod 4755 programa         # SUID + rwxr-xr-x           → rwsr-xr-x
$ chmod 2775 /srv/proyecto    # SGID + rwxrwxr-x           → rwxrwsr-x
$ chmod 1777 /srv/compartida  # sticky + rwxrwxrwx         → rwxrwxrwt
$ chmod 3770 /srv/dpto        # SGID + sticky + rwxrwx---  → rwxrws--T
```

!!! danger "Cuidado con el SUID"
    Un programa con SUID de `root` lo puede ejecutar cualquiera como si fuera administrador. Si ese programa tiene un fallo, alguien podría aprovecharlo para hacerse con el control del sistema. Por eso **nunca** se pone SUID a programas que no lo necesitan, y conviene revisar de vez en cuando cuáles lo tienen:
    ```bash
    $ sudo find / -perm -4000 -type f 2>/dev/null
    ```

## Caso práctico: carpeta compartida de un departamento

Queremos `/srv/informatica` donde:

- Todos los miembros del grupo `informatica` pueden crear ficheros.
- Los ficheros nuevos son del grupo `informatica` (**SGID**).
- Nadie puede borrar los ficheros de otro (***sticky bit***).
- El resto de usuarios no puede ni entrar.

```bash
$ sudo groupadd informatica
$ sudo mkdir /srv/informatica
$ sudo chown root:informatica /srv/informatica
$ sudo chmod 3770 /srv/informatica      # SGID + sticky + rwxrwx---
$ ls -ld /srv/informatica
drwxrws--T 2 root informatica 4096 ... /srv/informatica
```

La `T` mayúscula aparece porque "otros" no tienen `x`; aquí es lo que queremos.

## Resumen

| | SUID | SGID | *Sticky bit* |
|---|---|---|---|
| Octal | `4000` | `2000` | `1000` |
| Simbólico | `u+s` | `g+s` | `+t` |
| Se ve en | `x` del propietario | `x` del grupo | `x` de otros |
| En ficheros | Se ejecuta con los permisos del propietario | Se ejecuta con los permisos del grupo | Sin efecto |
| En directorios | Sin efecto | Lo nuevo hereda el grupo del directorio | Solo el propietario puede borrar sus ficheros |
| Ejemplo | `/usr/bin/passwd` | Carpetas compartidas | `/tmp` |

!!! note "Para saber más"
    [Permisos SGID, SUID y Sticky Bit en Linux](https://blog.deephacking.tech/es/posts/permisos-sgid-suid-stickybit/), de Deep Hacking.

## Ejercicios

**1.** Traduce a letras: `4755`, `2750`, `1777`, `4644`. ¿En cuál de ellos el permiso especial no sirve para nada?

??? success "Solución"
    `rwsr-xr-x`, `rwxr-s---`, `rwxrwxrwt`, `rwSr--r--`.
    En `4644` el SUID aparece como `S` mayúscula: el fichero no es ejecutable, así que el SUID no tiene efecto.

**2.** Traduce a octal: `rwsr-xr-x`, `rwxrwsr-x`, `rwxr-xr-t`.

??? success "Solución"
    `4755`, `2775`, `1755`.

**3.** Comprueba los permisos de `/usr/bin/passwd`, `/usr/bin/sudo` y `/tmp`. ¿Qué permiso especial tiene cada uno y para qué sirve?

??? success "Solución"
    ```bash
    $ ls -l /usr/bin/passwd /usr/bin/sudo
    $ ls -ld /tmp
    ```
    `passwd` y `sudo` tienen SUID de `root`: se ejecutan con privilegios de administrador para poder hacer su trabajo. `/tmp` tiene *sticky bit*: todos pueden crear ficheros, pero cada uno solo puede borrar los suyos.

**4.** Explica con tus palabras por qué un usuario puede cambiar su contraseña con `passwd` si `/etc/shadow` solo lo puede modificar `root`.

??? success "Solución"
    Porque `passwd` tiene SUID y su propietario es `root`: al ejecutarlo, funciona con los permisos de `root` y puede escribir en `/etc/shadow`. El programa solo deja a cada usuario cambiar su propia contraseña.

**5.** Busca en el sistema todos los ficheros con SUID. ¿Reconoces alguno?

??? success "Solución"
    ```bash
    $ sudo find / -perm -4000 -type f 2>/dev/null
    ```
    Suelen aparecer `passwd`, `sudo`, `su`, `mount`, `umount`, `chsh`... Son programas que un usuario normal tiene que poder usar, pero que necesitan privilegios de `root`.

**6.** Monta la carpeta compartida del caso práctico, pero para el grupo `asir1`, en `/srv/asir1`. Entra como `lucia`, crea un fichero y comprueba que su grupo es `asir1` y no `lucia`.

??? success "Solución"
    ```bash
    $ sudo mkdir /srv/asir1
    $ sudo chown root:asir1 /srv/asir1
    $ sudo chmod 3770 /srv/asir1
    $ su - lucia
    $ touch /srv/asir1/trabajo.txt
    $ ls -l /srv/asir1        # grupo asir1, gracias al SGID
    ```

**7.** Con otro usuario del grupo `asir1`, intenta borrar el fichero de `lucia`. ¿Qué pasa? ¿Por qué?

??? success "Solución"
    Obtiene `Operation not permitted`: el *sticky bit* impide borrar ficheros de otros, aunque tenga permiso de escritura en el directorio.

**8.** Quita el SGID de `/srv/asir1` (`sudo chmod g-s /srv/asir1`) y crea otro fichero como `lucia`. ¿De qué grupo es ahora? ¿Qué problema causa eso?

??? success "Solución"
    El fichero tiene como grupo `lucia` (su grupo primario). Los compañeros del grupo `asir1` no tienen permisos de grupo sobre él. Vuelve a ponerlo con `sudo chmod g+s /srv/asir1`.
