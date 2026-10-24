# 3.12 Ficheros de cuentas: `passwd`, `shadow`, `group` y `gshadow`

Los comandos del apartado anterior no hacen magia: todo lo que crean o modifican queda guardado en **cuatro ficheros de texto** dentro de `/etc`. Entenderlos permite consultar y diagnosticar cuentas con las herramientas de filtrado que ya conocemos.

| Fichero | Contenido | Permisos habituales |
|---|---|---|
| `/etc/passwd` | Usuarios | `-rw-r--r--` root root (lo puede leer cualquiera) |
| `/etc/shadow` | Contraseñas cifradas de los usuarios y su caducidad | `-rw-r-----` root shadow (solo root) |
| `/etc/group` | Grupos y sus miembros | `-rw-r--r--` root root |
| `/etc/gshadow` | Contraseñas y administradores de los grupos | `-rw-r-----` root shadow |

Todos tienen el mismo formato: **una línea por cuenta** y **campos separados por `:`**.

!!! danger "No los edites a mano"
    Usa los comandos (`useradd`, `usermod`, `passwd`...). Si alguna vez necesitas editarlos directamente, hazlo con `vipw` (para `passwd` y `shadow`) y `vigr` (para `group` y `gshadow`), que bloquean el fichero mientras lo editas. Un error de sintaxis puede dejar a todos los usuarios sin poder entrar.

## `/etc/passwd`

```text
lucia:x:1001:1001:Lucía Martí:/home/lucia:/bin/bash
```

| Campo | Valor | Significado |
|---|---|---|
| 1 | `lucia` | Nombre de usuario |
| 2 | `x` | Contraseña: la `x` indica que está en `/etc/shadow` |
| 3 | `1001` | UID |
| 4 | `1001` | GID del **grupo primario** |
| 5 | `Lucía Martí` | Comentario o GECOS (nombre completo, teléfono...) |
| 6 | `/home/lucia` | Directorio personal |
| 7 | `/bin/bash` | Shell de inicio |

Las cuentas de servicio suelen tener como shell `/usr/sbin/nologin` o `/bin/false`, que impide iniciar una sesión interactiva con ellas.

!!! note "¿Por qué una `x`?"
    Antiguamente la contraseña cifrada estaba en el campo 2 de `/etc/passwd`. Como ese fichero debe poder leerlo cualquiera (los programas lo consultan para convertir UID en nombres), las contraseñas se trasladaron a `/etc/shadow`, que solo puede leer `root`.

## `/etc/shadow`

```text
lucia:$y$j9T$Fq1...Ld0:20385:1:60:5:7:20999:
```

| Campo | Valor | Significado |
|---|---|---|
| 1 | `lucia` | Nombre de usuario |
| 2 | `$y$j9T$...` | Contraseña cifrada (*hash*) |
| 3 | `20385` | Último cambio de contraseña, en **días desde el 1/1/1970** |
| 4 | `1` | Días mínimos entre cambios |
| 5 | `60` | Días máximos de validez |
| 6 | `5` | Días de aviso antes de caducar |
| 7 | `7` | Días de inactividad permitidos tras caducar |
| 8 | `20999` | Fecha de expiración de la cuenta (días desde 1970) |
| 9 | | Reservado |

Son los mismos valores que vimos con `chage -l`, que los presenta de forma legible.

El campo 2 merece atención:

| Contenido | Significado |
|---|---|
| `$id$sal$hash` | Contraseña cifrada. El `id` indica el algoritmo: `$y$` yescrypt, `$6$` SHA-512, `$5$` SHA-256, `$1$` MD5 (obsoleto) |
| `!` o `*` | Sin contraseña válida: no se puede entrar con contraseña |
| `!` delante del hash | Cuenta **bloqueada** (`passwd -l` o `usermod -L` añaden este `!`) |
| Vacío | Sin contraseña: se entra sin ella (¡inseguro!) |

!!! tip "Convertir días en fechas"
    ```bash
    $ date -d "1970-01-01 +20385 days" +%d/%m/%Y
    24/10/2025
    ```

## `/etc/group`

```text
asir1:x:1002:lucia,pablo
```

| Campo | Valor | Significado |
|---|---|---|
| 1 | `asir1` | Nombre del grupo |
| 2 | `x` | Contraseña del grupo (está en `/etc/gshadow`) |
| 3 | `1002` | GID |
| 4 | `lucia,pablo` | Miembros **secundarios**, separados por comas |

!!! warning "El grupo primario no aparece aquí"
    El campo 4 solo lista a quienes tienen el grupo como **secundario**. Los usuarios cuyo grupo **primario** es ese se ven en el campo 4 de `/etc/passwd`. Por eso la línea del grupo `lucia` suele tener el campo de miembros vacío.

## `/etc/gshadow`

```text
asir1:!::lucia,pablo
```

| Campo | Significado |
|---|---|
| 1 | Nombre del grupo |
| 2 | Contraseña cifrada del grupo (`!` si no tiene) |
| 3 | **Administradores** del grupo (los que pueden gestionar miembros con `gpasswd`) |
| 4 | Miembros |

## `/etc/login.defs`

No guarda cuentas, sino los **valores por defecto** que usan los comandos de gestión de usuarios:

```bash
$ grep -Ev '^(#|$)' /etc/login.defs
```

| Directiva | Significado |
|---|---|
| `UID_MIN` / `UID_MAX` | Rango de UID para usuarios normales |
| `SYS_UID_MIN` / `SYS_UID_MAX` | Rango para cuentas del sistema |
| `GID_MIN` / `GID_MAX` | Igual para grupos |
| `PASS_MAX_DAYS`, `PASS_MIN_DAYS`, `PASS_WARN_AGE` | Caducidad por defecto de las contraseñas |
| `CREATE_HOME` | Si `useradd` crea el directorio personal sin `-m` |
| `USERGROUPS_ENAB` | Si se crea un grupo con el mismo nombre que el usuario |
| `ENCRYPT_METHOD` | Algoritmo de cifrado de las contraseñas |

## Consultar las cuentas: `getent`

Las cuentas no siempre están solo en estos ficheros: en una empresa o un centro educativo pueden venir de un servidor LDAP o de un dominio. El sistema reúne todas las fuentes mediante el **NSS** (*Name Service Switch*, configurado en `/etc/nsswitch.conf`). `getent` consulta esas bases de datos **igual que lo hace el sistema**, sea cual sea su origen:

```bash
$ getent passwd lucia
$ getent group asir1
$ sudo getent shadow lucia
$ getent passwd | wc -l           # todas las cuentas
```

Por eso es más fiable que `grep lucia /etc/passwd`.

## Filtrar las bases de datos

Con lo que vimos en la Parte 1 podemos obtener mucha información:

```bash
$ cut -d: -f1 /etc/passwd                                  # todos los usuarios
$ awk -F: '$3 >= 1000 && $3 < 65534 {print $1}' /etc/passwd   # usuarios normales
$ grep -E ':/bin/(ba|z)?sh$' /etc/passwd | cut -d: -f1     # con shell interactivo
$ cut -d: -f7 /etc/passwd | sort | uniq -c                 # shells en uso
$ getent group sudo | cut -d: -f4                          # quién puede usar sudo
$ sudo awk -F: '$2 ~ /^!/ {print $1}' /etc/shadow          # cuentas bloqueadas
$ sudo awk -F: '$2 == "" {print $1}' /etc/shadow           # cuentas sin contraseña
```

!!! info "`awk`"
    `awk` es un lenguaje de procesamiento de texto que trabaja por campos. En `awk -F: '$3 >= 1000 {print $1}'`, `-F:` indica el separador, `$3` es el tercer campo y `{print $1}` imprime el primero. Para filtrar por números es más cómodo que `grep`.

## Resumen

| Fichero | Clave para recordarlo |
|---|---|
| `/etc/passwd` | 7 campos: usuario, x, UID, GID, GECOS, home, shell |
| `/etc/shadow` | 9 campos: usuario, hash, y 7 campos de fechas en días |
| `/etc/group` | 4 campos: grupo, x, GID, miembros secundarios |
| `/etc/gshadow` | 4 campos: grupo, contraseña, administradores, miembros |
| `/etc/login.defs` | Valores por defecto de `useradd` y compañía |
| `getent` | Consultar cuentas a través del NSS |
| `vipw`, `vigr` | Editar los ficheros de forma segura |

## Ejercicios

**1.** Comprueba los permisos de los cuatro ficheros de cuentas. ¿Por qué `/etc/shadow` no puede leerlo un usuario normal y `/etc/passwd` sí?

??? success "Solución"
    ```bash
    $ ls -l /etc/passwd /etc/shadow /etc/group /etc/gshadow
    ```
    `/etc/shadow` contiene los *hashes* de las contraseñas: si cualquiera los pudiera leer, podría intentar descifrarlos por fuerza bruta. `/etc/passwd` lo necesitan muchos programas para traducir UID a nombres, así que tiene que ser legible para todos.

**2.** Interpreta esta línea:

```text
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
```

??? success "Solución"
    Es el usuario `www-data` (el del servidor web en Debian y Ubuntu), con UID 33 y grupo primario 33. Su directorio personal es `/var/www` y su shell `/usr/sbin/nologin`, así que no se puede iniciar sesión con él. Por su UID (< 1000) es una cuenta del sistema.

**3.** Muestra, para la usuaria `lucia` creada en el apartado anterior, su línea de `passwd`, de `shadow` y los grupos en los que aparece en `/etc/group`. Usa `getent`.

??? success "Solución"
    ```bash
    $ getent passwd lucia
    $ sudo getent shadow lucia
    $ getent group | grep -w lucia
    ```

**4.** Bloquea la cuenta de `lucia` con `passwd -l` y observa qué cambia en su línea de `/etc/shadow`. Desbloquéala después.

??? success "Solución"
    ```bash
    $ sudo passwd -l lucia
    $ sudo getent shadow lucia      # el hash empieza ahora por !
    $ sudo passwd -u lucia
    ```

**5.** ¿Qué algoritmo de cifrado usa tu sistema para las contraseñas? Compruébalo en `/etc/shadow` y en `/etc/login.defs`.

??? success "Solución"
    ```bash
    $ sudo grep "^$USER:" /etc/shadow | cut -d: -f2 | cut -c1-3
    $ grep ENCRYPT_METHOD /etc/login.defs
    ```
    `$y$` es yescrypt (Debian 11+ y Ubuntu 22.04+); `$6$` es SHA-512.

**6.** ¿En qué fecha cambió `lucia` su contraseña por última vez? Calcúlalo a partir del campo 3 de `/etc/shadow` y compáralo con `chage -l`.

??? success "Solución"
    ```bash
    $ dias=$(sudo getent shadow lucia | cut -d: -f3)
    $ date -d "1970-01-01 +$dias days" +%d/%m/%Y
    $ sudo chage -l lucia
    ```

**7.** Lista solo los usuarios **normales** del sistema (UID entre `UID_MIN` y `UID_MAX`).

??? success "Solución"
    ```bash
    $ grep -E '^UID_(MIN|MAX)' /etc/login.defs
    $ awk -F: '$3 >= 1000 && $3 <= 60000 {print $1, $3}' /etc/passwd
    ```

**8.** ¿Cuántas cuentas del sistema no pueden iniciar sesión (shell `nologin` o `false`)?

??? success "Solución"
    ```bash
    $ grep -Ec '(nologin|false)$' /etc/passwd
    ```

**9.** Muestra los miembros del grupo `sudo` (o `wheel`). ¿Por qué podría haber un usuario con permisos de `sudo` que no aparezca en esa lista?

??? success "Solución"
    ```bash
    $ getent group sudo
    ```
    Porque `/etc/group` solo muestra los miembros secundarios. También podría tener permisos concedidos directamente en `/etc/sudoers` o en un fichero de `/etc/sudoers.d/`.

**10.** Busca si hay cuentas **sin contraseña** o con el UID 0 aparte de `root`. ¿Por qué serían un problema de seguridad?

??? success "Solución"
    ```bash
    $ sudo awk -F: '$2 == "" {print $1}' /etc/shadow
    $ awk -F: '$3 == 0 {print $1}' /etc/passwd
    ```
    Una cuenta sin contraseña permite entrar a cualquiera. Una cuenta con UID 0 es, a todos los efectos, `root`, aunque se llame de otra forma: es una técnica habitual para dejar una puerta trasera.
