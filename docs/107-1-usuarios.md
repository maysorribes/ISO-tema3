# 3.11 Gestión de usuarios y grupos

Linux es un sistema **multiusuario**: varias personas (y muchos servicios) comparten la misma máquina, cada uno con su identidad, sus ficheros y sus permisos. En este apartado veremos cómo crear, modificar y eliminar cuentas de usuario y grupos desde la terminal.

!!! warning "Necesitas privilegios"
    Casi todos los comandos de este apartado modifican ficheros del sistema, así que hay que ejecutarlos como `root` o con `sudo`. Practica en una máquina virtual.

## Conceptos básicos

| Concepto | Qué es |
|---|---|
| **Usuario** | Identidad con un nombre (`alumno`) y un número, el **UID** |
| **Grupo** | Conjunto de usuarios, con un nombre y un número, el **GID** |
| **Grupo primario** | El grupo principal del usuario; es el que se asigna a los ficheros que crea. Solo hay uno |
| **Grupos secundarios** | Otros grupos a los que pertenece, para obtener permisos adicionales |
| **`root`** | El superusuario. Siempre tiene UID 0 |

Rangos de UID habituales (se definen en `/etc/login.defs`):

| UID | Tipo de cuenta |
|---|---|
| `0` | `root` |
| `1`–`999` | Cuentas del sistema (servicios como `www-data`, `sshd`...) |
| `1000` en adelante | Usuarios normales |

### ¿Quién soy?

```bash
$ whoami                 # nombre de usuario
alumno
$ id                     # UID, GID y todos los grupos
uid=1000(alumno) gid=1000(alumno) grupos=1000(alumno),27(sudo),100(users)
$ id ana                 # los de otro usuario
$ groups                 # solo los nombres de los grupos
$ who                    # quién está conectado
```

## Crear usuarios: `useradd`

```bash
$ sudo useradd -m -s /bin/bash -c "Ana García" ana
```

Opciones más importantes:

| Opción | Efecto |
|---|---|
| `-m` | Crea el directorio personal (copiando el contenido de `/etc/skel`) |
| `-d ruta` | Usa otra ruta como directorio personal |
| `-s shell` | Shell de inicio de sesión |
| `-c "texto"` | Comentario (normalmente el nombre completo) |
| `-u UID` | UID concreto |
| `-g grupo` | Grupo primario |
| `-G g1,g2` | Grupos secundarios |
| `-e AAAA-MM-DD` | Fecha de caducidad de la cuenta |
| `-r` | Crea una cuenta del sistema |
| `-D` | Muestra (o cambia) los valores por defecto |

!!! info "Grupo privado de usuario"
    En la mayoría de distribuciones, al crear el usuario `ana` se crea también el grupo `ana`, que será su grupo primario. Lo controla la opción `USERGROUPS_ENAB` de `/etc/login.defs`.

Después de crearlo hay que **asignarle una contraseña**; mientras no la tenga, no podrá iniciar sesión:

```bash
$ sudo passwd ana
```

!!! tip "`adduser` en Debian y Ubuntu"
    Debian y Ubuntu incluyen `adduser`, un programa más amigable que pregunta los datos (contraseña, nombre...) y crea el directorio personal automáticamente: `sudo adduser ana`. En el examen LPIC y en otras distribuciones el comando estándar es `useradd`.

### Valores por defecto y `/etc/skel`

```bash
$ useradd -D                 # valores por defecto de useradd
$ ls -la /etc/skel           # plantilla del directorio personal
```

Todo lo que pongas en `/etc/skel` (un `.bashrc` personalizado, una carpeta `Documentos`...) se copiará al directorio personal de cada usuario **nuevo**.

## Modificar usuarios: `usermod`

Usa casi las mismas opciones que `useradd`, más algunas propias:

| Opción | Efecto |
|---|---|
| `-c`, `-s`, `-u`, `-g`, `-e` | Igual que en `useradd` |
| `-G g1,g2` | **Sustituye** la lista de grupos secundarios |
| `-a -G grupo` | **Añade** a un grupo secundario, conservando los demás |
| `-l nuevo` | Cambia el nombre de usuario |
| `-d ruta -m` | Cambia el directorio personal y mueve su contenido |
| `-L` | Bloquea la cuenta |
| `-U` | Desbloquea la cuenta |

```bash
$ sudo usermod -aG sudo ana               # ana puede usar sudo
$ sudo usermod -s /bin/zsh ana
$ sudo usermod -c "Ana García López" ana
$ sudo usermod -L ana                     # bloquear
$ sudo usermod -U ana                     # desbloquear
```

!!! danger "`-G` sin `-a`"
    `usermod -G docker ana` deja a `ana` **solo** en el grupo `docker`, quitándola de todos los demás grupos secundarios (incluido `sudo`). Para añadir, usa siempre `-aG`.

Los cambios de grupo no se aplican a las sesiones abiertas: el usuario debe cerrar sesión y volver a entrar (o usar `newgrp grupo` en esa terminal).

## Eliminar usuarios: `userdel`

```bash
$ sudo userdel ana          # borra la cuenta, pero deja su directorio personal
$ sudo userdel -r ana       # borra también su directorio personal y su buzón
```

Los ficheros que el usuario tuviera **fuera** de su directorio personal no se borran: quedan con su antiguo UID como propietario. Se pueden buscar con `sudo find / -nouser`.

## Gestionar grupos

```bash
$ sudo groupadd profesores               # crear
$ sudo groupadd -g 2000 alumnos          # con un GID concreto
$ sudo groupmod -n docentes profesores   # renombrar
$ sudo groupmod -g 2001 docentes         # cambiar el GID
$ sudo groupdel docentes                 # eliminar
```

No se puede borrar un grupo que sea el **grupo primario** de algún usuario.

### Miembros de un grupo: `gpasswd`

```bash
$ sudo gpasswd -a ana alumnos        # añadir a ana al grupo
$ sudo gpasswd -d ana alumnos        # quitarla
$ sudo gpasswd -M ana,luis alumnos   # fijar la lista completa de miembros
$ sudo gpasswd -A luis alumnos       # luis pasa a administrar el grupo
$ getent group alumnos               # ver los miembros
```

Un **administrador de grupo** puede añadir y quitar miembros sin ser `root`.

## Contraseñas y caducidad

### `passwd`

```bash
$ passwd                     # cambiar mi propia contraseña
$ sudo passwd ana            # cambiar la de otro (solo root)
$ sudo passwd -l ana         # bloquear la contraseña
$ sudo passwd -u ana         # desbloquearla
$ sudo passwd -S ana         # estado de la cuenta
$ sudo passwd -e ana         # obligar a cambiarla en el próximo inicio de sesión
$ sudo passwd -d ana         # quitar la contraseña (¡peligroso!)
```

### `chage`: política de caducidad

```bash
$ sudo chage -l ana                 # ver la política actual
$ sudo chage -M 90 ana              # caduca a los 90 días
$ sudo chage -m 1 ana               # mínimo 1 día entre cambios
$ sudo chage -W 7 ana               # avisar 7 días antes
$ sudo chage -I 5 ana               # 5 días de margen tras caducar; luego se inhabilita
$ sudo chage -E 2027-06-30 ana      # la cuenta expira en esa fecha
$ sudo chage -d 0 ana               # forzar el cambio en el próximo inicio de sesión
$ sudo chage ana                    # modo interactivo
```

!!! note "Contraseña frente a cuenta"
    Caducar la **contraseña** (`-M`) obliga a cambiarla. Expirar la **cuenta** (`-E`) impide entrar del todo, aunque la contraseña sea correcta. Es útil para alumnos o personal temporal.

## Cambiar de usuario: `su` y `sudo`

```bash
$ su - ana             # abrir una sesión como ana (pide la contraseña de ana)
$ su -                 # convertirse en root (pide la contraseña de root)
$ sudo comando         # ejecutar un comando como root (pide TU contraseña)
$ sudo -u ana comando  # ejecutar un comando como ana
$ sudo -i              # shell de root
```

El guion de `su -` hace que se cargue el entorno completo del otro usuario (su `PATH`, su directorio personal...). Quién puede usar `sudo` se define en `/etc/sudoers` (se edita siempre con `visudo`) y, en Debian y Ubuntu, perteneciendo al grupo `sudo` (`wheel` en Red Hat y derivadas).

## Resumen de comandos

| Comando | Uso |
|---|---|
| `id`, `whoami`, `groups`, `who` | Ver identidad y grupos |
| `useradd` / `adduser` | Crear usuarios |
| `usermod` | Modificar usuarios (`-aG` para añadir a un grupo) |
| `userdel -r` | Eliminar usuarios y su directorio personal |
| `groupadd`, `groupmod`, `groupdel` | Crear, modificar y eliminar grupos |
| `gpasswd` | Gestionar los miembros y administradores de un grupo |
| `passwd` | Cambiar, bloquear o forzar el cambio de contraseña |
| `chage` | Política de caducidad de contraseñas y cuentas |
| `su`, `sudo` | Actuar como otro usuario |

## Ejercicios

**1.** Muestra tu UID, tu grupo primario y todos tus grupos secundarios. ¿Puedes usar `sudo`? ¿Cómo lo sabes?

??? success "Solución"
    ```bash
    $ id
    ```
    Si aparece el grupo `sudo` (o `wheel`), puedes usar `sudo`.

**2.** Crea los grupos `asir1` y `asir2`, este último con GID 3002.

??? success "Solución"
    ```bash
    $ sudo groupadd asir1
    $ sudo groupadd -g 3002 asir2
    $ getent group asir1 asir2
    ```

**3.** Crea el usuario `lucia`, con directorio personal, shell Bash, nombre completo "Lucía Martí" y `asir1` como grupo secundario. Asígnale una contraseña y comprueba que puedes entrar con `su - lucia`.

??? success "Solución"
    ```bash
    $ sudo useradd -m -s /bin/bash -c "Lucía Martí" -G asir1 lucia
    $ sudo passwd lucia
    $ su - lucia
    $ id
    $ exit
    ```

**4.** Antes de crear más usuarios, haz que todos los nuevos tengan en su directorio personal una carpeta `practicas` y un fichero `LEEME.txt` con el texto `Bienvenido al aula`. Crea el usuario `pablo` y compruébalo.

??? success "Solución"
    ```bash
    $ sudo mkdir /etc/skel/practicas
    $ echo "Bienvenido al aula" | sudo tee /etc/skel/LEEME.txt
    $ sudo useradd -m -s /bin/bash pablo
    $ sudo ls -l /home/pablo
    ```
    `lucia` no los tiene: `/etc/skel` solo se copia al crear el usuario.

**5.** Añade a `lucia` también al grupo `asir2` **sin** quitarla de `asir1`. Comprueba sus grupos.

??? success "Solución"
    ```bash
    $ sudo usermod -aG asir2 lucia
    $ id lucia
    ```

**6.** Ahora ejecuta `sudo usermod -G asir2 lucia` (sin `-a`) y vuelve a mirar sus grupos. ¿Qué ha pasado? Déjala otra vez en los dos grupos.

??? success "Solución"
    Ha perdido `asir1`: `-G` sin `-a` sustituye la lista completa de grupos secundarios.
    ```bash
    $ sudo usermod -G asir1,asir2 lucia
    ```

**7.** Configura la cuenta de `pablo` para que la contraseña caduque cada 60 días, avise con 5 días de antelación, obligue a cambiarla en el primer inicio de sesión y la cuenta expire al final del curso (30 de junio de 2027). Comprueba la configuración.

??? success "Solución"
    ```bash
    $ sudo chage -M 60 -W 5 -d 0 -E 2027-06-30 pablo
    $ sudo chage -l pablo
    ```

**8.** Bloquea la cuenta de `pablo`, comprueba que no puede entrar con `su - pablo` y desbloquéala.

??? success "Solución"
    ```bash
    $ sudo usermod -L pablo       # o: sudo passwd -l pablo
    $ sudo passwd -S pablo        # aparece L (locked)
    $ su - pablo                  # falla la autenticación
    $ sudo usermod -U pablo
    ```

**9.** Haz que `lucia` sea administradora del grupo `asir1`. Entra como `lucia` y añade a `pablo` a ese grupo sin usar `sudo`.

??? success "Solución"
    ```bash
    $ sudo gpasswd -A lucia asir1
    $ su - lucia
    $ gpasswd -a pablo asir1
    $ exit
    $ getent group asir1
    ```

**10.** Elimina el usuario `pablo` con su directorio personal y el grupo `asir2`. ¿Por qué no puedes eliminar el grupo `lucia`?

??? success "Solución"
    ```bash
    $ sudo userdel -r pablo
    $ sudo groupdel asir2
    $ sudo groupdel lucia
    groupdel: cannot remove the primary group of user 'lucia'
    ```
    El grupo `lucia` es el grupo primario de la usuaria `lucia`.
