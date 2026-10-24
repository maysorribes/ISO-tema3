# 3.1 Variables y caracteres especiales

Cuando abrimos una terminal, el shell (normalmente **Bash**) no arranca "vacío": trae consigo un conjunto de **variables** que guardan información sobre la sesión, el usuario y el sistema. Muchos programas leen esas variables para saber cómo comportarse.

## Variables de entorno

Una variable es un **nombre** asociado a un **valor**. Algunas de las más habituales:

| Variable | Qué guarda |
|---|---|
| `HOME` | Directorio personal del usuario |
| `USER` | Nombre del usuario |
| `PWD` | Directorio de trabajo actual |
| `SHELL` | Shell por defecto del usuario |
| `PATH` | Directorios donde el shell busca los programas |
| `LANG` | Idioma y codificación |

### Consultar variables: `env` y `echo`

`env` muestra todas las variables de entorno de la sesión:

```bash
$ env
```

Para ver una sola, usamos `echo` con el nombre de la variable precedido de `$`. El shell **expande** `$NOMBRE` y lo sustituye por su valor antes de ejecutar el comando:

```bash
$ echo $HOME
/home/alumno
$ echo "Hola, soy $USER y estoy en $PWD"
Hola, soy alumno y estoy en /home/alumno
```

### La variable `PATH`

`PATH` contiene una lista de directorios separados por `:`. Cuando escribimos un comando como `ls`, el shell lo busca en esos directorios, en orden, y ejecuta el primero que encuentra:

```bash
$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

Gracias a `PATH` no tenemos que escribir `/usr/bin/ls`: basta con `ls`. Si un programa no está en ninguno de esos directorios, hay que indicar su ruta (por ejemplo `./miscript.sh`).

!!! tip "¿Dónde está un comando?"
    `which ls` o `type ls` te dicen qué fichero se ejecuta realmente al escribir `ls`.

## Crear variables

Se asigna con `=`, **sin espacios** alrededor:

```bash
$ ciclo=ASIR
$ echo $ciclo
ASIR
```

!!! warning "Sin espacios"
    `ciclo = ASIR` da error: Bash interpreta `ciclo` como un comando al que se le pasan los argumentos `=` y `ASIR`.

### Variables locales y exportadas

Una variable creada así es **local**: solo existe en el shell actual. Si abrimos un shell hijo (escribiendo `bash`), no la verá:

```bash
$ ciclo=ASIR
$ bash          # abrimos un shell hijo
$ echo $ciclo   # no muestra nada

$ exit          # volvemos al shell padre
```

Para que la variable pase a los procesos hijos hay que **exportarla**:

```bash
$ export ciclo
$ bash
$ echo $ciclo
ASIR
$ exit
```

También se puede crear y exportar a la vez: `export ciclo=ASIR`.

!!! note "Esto es temporal"
    Todo lo que hagas así desaparece al cerrar la sesión. Para hacerlo permanente se añade a ficheros como `~/.bashrc` (lo veremos más adelante).

### Añadir un directorio al `PATH`

Un uso muy común de `export` es ampliar el `PATH` sin perder lo que ya tenía:

```bash
$ mkdir ~/bin
$ export PATH="$HOME/bin:$PATH"
```

A partir de ese momento, cualquier script ejecutable que pongas en `~/bin` se podrá lanzar desde cualquier directorio.

## Eliminar variables: `unset`

```bash
$ unset ciclo
$ echo $ciclo

```

Fíjate en que a `unset` se le pasa el **nombre**, sin `$`.

## `env` frente a `set`

| Comando | Qué muestra |
|---|---|
| `env` | Solo las variables **exportadas** (las que heredan los procesos hijos) |
| `set` | **Todas** las variables del shell (locales y exportadas) y también las funciones |

Podemos comprobarlo filtrando con `grep`:

```bash
$ prueba=hola        # variable local, sin exportar
$ env | grep prueba  # no aparece
$ set | grep prueba
prueba=hola
```

## Caracteres especiales, comillas y escape

Bash da un significado especial a ciertos caracteres. Por ejemplo, el **espacio** separa argumentos. Si hacemos:

```bash
$ touch notas de clase
$ ls
clase  de  notas
```

hemos creado **tres** ficheros, no uno. Otros caracteres especiales son: `$ * ? [ ] ' " \ | & ; < > ( ) { } # ~ !`

Para que Bash los trate de forma literal tenemos tres opciones:

=== "Comillas dobles"

    ```bash
    $ touch "notas de clase"
    ```
    Protegen casi todo, **excepto** `$`, `` ` `` y `\`. Por eso las variables **sí** se expanden:
    ```bash
    $ echo "Mi casa es $HOME"
    Mi casa es /home/alumno
    ```

=== "Comillas simples"

    ```bash
    $ touch 'notas de clase'
    ```
    Protegen **todo**: nada se expande.
    ```bash
    $ echo 'Mi casa es $HOME'
    Mi casa es $HOME
    ```

=== "Barra invertida"

    ```bash
    $ touch notas\ de\ clase
    ```
    `\` hace literal **solo el carácter siguiente**.
    ```bash
    $ echo "Esto cuesta \$5"
    Esto cuesta $5
    ```

## Resumen de comandos

| Comando | Uso |
|---|---|
| `echo` | Muestra texto y el valor de variables |
| `env` | Lista las variables de entorno |
| `set` | Lista todas las variables y funciones del shell |
| `export` | Hace que una variable pase a los procesos hijos |
| `unset` | Elimina una variable |

## Ejercicios

**1.** Muestra con un solo `echo` la frase: `El usuario X tiene su directorio personal en Y`, donde X e Y salgan de variables.

??? success "Solución"
    ```bash
    $ echo "El usuario $USER tiene su directorio personal en $HOME"
    ```

**2.** Crea una variable `modulo` con el valor `ISO`. Comprueba si aparece con `env` y con `set`. Después expórtala y repite la comprobación. Explica la diferencia.

??? success "Solución"
    ```bash
    $ modulo=ISO
    $ env | grep modulo     # nada: es local
    $ set | grep modulo     # modulo=ISO
    $ export modulo
    $ env | grep modulo     # modulo=ISO
    ```
    Antes de exportarla es una variable local: `set` la ve, `env` no. Al exportarla pasa a ser de entorno y ya aparece en ambos.

**3.** Crea el directorio `~/scripts` y dentro un script `saludo.sh` que muestre `Hola`. Hazlo ejecutable y consigue lanzarlo escribiendo solo `saludo.sh` desde cualquier directorio.

??? success "Solución"
    ```bash
    $ mkdir ~/scripts
    $ echo '#!/bin/bash' > ~/scripts/saludo.sh
    $ echo 'echo Hola' >> ~/scripts/saludo.sh
    $ chmod +x ~/scripts/saludo.sh
    $ export PATH="$HOME/scripts:$PATH"
    $ cd /tmp
    $ saludo.sh
    Hola
    ```

**4.** Ejecuta `unset PATH` y prueba a lanzar `ls`. ¿Qué ocurre y por qué? ¿Cómo podrías ejecutar `ls` igualmente? (Para recuperar el estado normal, cierra la terminal.)

??? success "Solución"
    El shell responde `ls: No such file or directory` (o `command not found`) porque ya no sabe en qué directorios buscar los programas. Se puede ejecutar dando la ruta absoluta: `/usr/bin/ls` (o `/bin/ls`).

**5.** Predice la salida de cada línea y compruébalo:

```bash
$ nombre=Ana
$ echo "Hola $nombre"
$ echo 'Hola $nombre'
$ echo Hola \$nombre
```

??? success "Solución"
    ```
    Hola Ana
    Hola $nombre
    Hola $nombre
    ```

**6.** Crea un fichero llamado `informe final 2026.txt` usando las tres formas de proteger los espacios (borra el anterior entre intento e intento con `rm`).

??? success "Solución"
    ```bash
    $ touch "informe final 2026.txt"
    $ rm "informe final 2026.txt"
    $ touch 'informe final 2026.txt'
    $ rm 'informe final 2026.txt'
    $ touch informe\ final\ 2026.txt
    ```
