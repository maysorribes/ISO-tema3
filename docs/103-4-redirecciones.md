# 3.5 Redirecciones

En el apartado de filtros vimos por encima `>`, `>>` y `<`. Aquí los estudiamos a fondo: cómo controlar **de dónde lee** un programa y **adónde escribe** tanto su salida normal como sus errores.

## Descriptores de fichero

Cada proceso tiene abiertos, como mínimo, tres canales. Cada uno se identifica con un número, el **descriptor de fichero**:

| Descriptor | Nombre | Por defecto | Para qué |
|---|---|---|---|
| `0` | `stdin` (entrada estándar) | Teclado | Datos que lee el programa |
| `1` | `stdout` (salida estándar) | Pantalla | Resultados normales |
| `2` | `stderr` (salida de error) | Pantalla | Mensajes de error y avisos |

Como `stdout` y `stderr` van por defecto a la pantalla, a simple vista no se distinguen. Pero son canales distintos y se pueden redirigir por separado:

```bash
$ ls /etc/hostname /noexiste
ls: cannot access '/noexiste': No such file or directory    ← stderr
/etc/hostname                                                ← stdout
```

## Redirigir la salida estándar

| Operador | Efecto |
|---|---|
| `>` o `1>` | Envía `stdout` a un fichero. Si existe, **lo vacía** antes |
| `>>` o `1>>` | Envía `stdout` al **final** del fichero, sin borrar lo que hubiera |

```bash
$ ls /etc > listado.txt          # crea o sobrescribe
$ date >> registro.log           # añade una línea cada vez
$ > vacio.txt                    # crea un fichero vacío (o vacía uno existente)
```

!!! warning "`>` no avisa"
    Si te equivocas y escribes `sort datos.txt > datos.txt`, perderás el contenido: el shell vacía `datos.txt` **antes** de que `sort` lo lea.

### Protección con `noclobber`

La opción `noclobber` de Bash impide que `>` sobrescriba ficheros existentes:

```bash
$ set -o noclobber
$ echo hola > listado.txt
bash: listado.txt: cannot overwrite existing file
$ echo hola >| listado.txt       # >| fuerza la sobrescritura
$ set +o noclobber               # desactiva la protección
```

## Redirigir los errores

Se indica el descriptor `2` delante del operador:

```bash
$ find / -name "*.conf" 2> errores.txt      # resultados en pantalla, errores al fichero
$ find / -name "*.conf" 2>> errores.txt     # añadiendo
$ find / -name "*.conf" > ok.txt 2> mal.txt # cada canal a su fichero
```

### Descartar la salida: `/dev/null`

`/dev/null` es un fichero especial que **descarta** todo lo que se escribe en él. Es la "papelera" para salidas que no nos interesan:

```bash
$ find / -name "*.conf" 2> /dev/null        # oculta los "Permission denied"
$ ping -c 1 8.8.8.8 > /dev/null             # solo nos interesa si funciona o no
```

## Juntar salida y errores

A veces queremos todo en el mismo sitio, por ejemplo en un log:

```bash
$ comando > todo.log 2>&1      # forma clásica (POSIX)
$ comando &> todo.log          # atajo de Bash, equivalente
$ comando &>> todo.log         # añadiendo
```

`2>&1` significa "envía el descriptor 2 **al mismo sitio** al que apunta ahora el descriptor 1".

!!! danger "El orden importa"
    Las redirecciones se procesan **de izquierda a derecha**:

    - `comando > todo.log 2>&1` → primero `stdout` va al fichero y después `stderr` va adonde está `stdout` (el fichero). **Todo al fichero.**
    - `comando 2>&1 > todo.log` → primero `stderr` va adonde está `stdout` (la pantalla) y después `stdout` cambia al fichero. **Los errores siguen en pantalla.**

## Redirigir la entrada

### Desde un fichero: `<`

```bash
$ wc -l < /etc/passwd        # wc lee de stdin; no muestra el nombre del fichero
$ sort < nombres.txt > ordenados.txt
$ tr 'a-z' 'A-Z' < notas.txt
```

### Documento en línea (*here document*): `<<`

Permite escribir varias líneas de entrada directamente en la terminal o en un script, hasta una palabra que marca el final (por convenio `EOF`):

```bash
$ cat << EOF > saludo.txt
Hola, $USER
Hoy es $(date +%A)
EOF
$ cat saludo.txt
Hola, alumno
Hoy es sábado
```

Las variables se expanden. Si ponemos el delimitador entre comillas (`<< 'EOF'`), el texto se toma literalmente. Con `<<-` se ignoran los tabuladores iniciales, útil para sangrar el texto dentro de un script.

### Cadena en línea (*here string*): `<<<`

Pasa **una sola cadena** como entrada estándar:

```bash
$ wc -w <<< "esto son cinco palabras aquí"
5
$ tr 'a-z' 'A-Z' <<< "$USER"
ALUMNO
```

## Otros descriptores

Además de 0, 1 y 2 podemos abrir descriptores propios (3 a 9) con `exec`. Es algo propio de scripts avanzados, pero conviene reconocerlo:

```bash
$ exec 3> salida3.txt     # abre el descriptor 3 hacia un fichero
$ echo "por el 3" >&3     # escribe en él
$ exec 3>&-               # lo cierra
```

## Resumen de operadores

| Operador | Significado |
|---|---|
| `>` / `>>` | `stdout` a fichero (sobrescribir / añadir) |
| `2>` / `2>>` | `stderr` a fichero (sobrescribir / añadir) |
| `&>` / `&>>` | `stdout` y `stderr` a fichero (Bash) |
| `> f 2>&1` | `stdout` y `stderr` a fichero (POSIX) |
| `>|` | Sobrescribir aunque esté activo `noclobber` |
| `<` | `stdin` desde fichero |
| `<< FIN` | `stdin` desde las líneas siguientes hasta `FIN` |
| `<<< "texto"` | `stdin` desde una cadena |
| `/dev/null` | Descarta lo que recibe |

## Ejercicios

**1.** Ejecuta `ls /etc/passwd /etc/noexiste`. Consigue que el resultado correcto vaya a `bien.txt` y el error a `mal.txt`. Comprueba ambos ficheros.

??? success "Solución"
    ```bash
    $ ls /etc/passwd /etc/noexiste > bien.txt 2> mal.txt
    $ cat bien.txt mal.txt
    ```

**2.** Busca en `/` todos los ficheros llamados `hosts` mostrando solo los resultados, sin ningún error de permisos.

??? success "Solución"
    ```bash
    $ find / -name hosts 2> /dev/null
    ```

**3.** Crea un fichero `registro.log` y añade tres veces la fecha y hora actual. Comprueba que tiene tres líneas.

??? success "Solución"
    ```bash
    $ date >> registro.log
    $ date >> registro.log
    $ date >> registro.log
    $ wc -l registro.log
    ```

**4.** Guarda en `todo.log`, con **una** redirección de Bash, la salida y los errores de `ls /etc/hostname /nada`. Después hazlo con la forma POSIX.

??? success "Solución"
    ```bash
    $ ls /etc/hostname /nada &> todo.log
    $ ls /etc/hostname /nada > todo.log 2>&1
    ```

**5.** Explica por qué estos dos comandos se comportan de forma distinta:

```bash
$ ls /etc/hostname /nada > f.txt 2>&1
$ ls /etc/hostname /nada 2>&1 > f.txt
```

??? success "Solución"
    En el primero, `stdout` se dirige a `f.txt` y luego `stderr` se copia hacia donde apunta `stdout` (`f.txt`): todo acaba en el fichero. En el segundo, `stderr` se copia primero hacia donde apunta `stdout` en ese momento (la pantalla) y después `stdout` pasa a `f.txt`: el error se ve en pantalla.

**6.** Activa `noclobber`, intenta sobrescribir `registro.log` con `echo` y fuérzalo después. Desactiva la opción al terminar.

??? success "Solución"
    ```bash
    $ set -o noclobber
    $ echo nuevo > registro.log      # error
    $ echo nuevo >| registro.log     # funciona
    $ set +o noclobber
    ```

**7.** Con un *here document*, crea `ficha.txt` con tres líneas: tu usuario, tu directorio personal y el nombre de la máquina (`$HOSTNAME`), usando variables.

??? success "Solución"
    ```bash
    $ cat << EOF > ficha.txt
    Usuario: $USER
    Home: $HOME
    Equipo: $HOSTNAME
    EOF
    ```

**8.** Repite el ejercicio anterior poniendo el delimitador entre comillas simples (`<< 'EOF'`). ¿Qué cambia?

??? success "Solución"
    Las variables no se expanden: el fichero contiene literalmente `$USER`, `$HOME` y `$HOSTNAME`.

**9.** Usando una *here string*, cuenta cuántos caracteres tiene el contenido de la variable `HOME`.

??? success "Solución"
    ```bash
    $ wc -c <<< "$HOME"
    ```
    El resultado incluye un carácter más por el salto de línea que añade `<<<`. Sin él: `echo -n "$HOME" | wc -c`.
