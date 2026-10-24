# 3.2 Filtros de texto

Una de las ideas centrales de Unix (y por tanto de Linux) es que cada programa haga **una sola cosa y la haga bien**, y que los programas se puedan **combinar** entre sí pasándose texto. A esos programas que reciben texto, lo transforman y lo devuelven los llamamos **filtros**.

## Entrada, salida, redirecciones y tuberías

Todo programa tiene tres canales:

| Canal | Nombre | Por defecto |
|---|---|---|
| 0 | Entrada estándar (`stdin`) | Teclado |
| 1 | Salida estándar (`stdout`) | Pantalla |
| 2 | Salida de error (`stderr`) | Pantalla |

Podemos cambiar hacia dónde van con estos operadores (los veremos a fondo en los apartados 3.5 y 3.6):

| Operador | Efecto | Ejemplo |
|---|---|---|
| `>` | Envía la salida a un fichero (lo **sobrescribe**) | `ls > lista.txt` |
| `>>` | Añade la salida al **final** del fichero | `date >> registro.txt` |
| `<` | Toma la entrada desde un fichero | `sort < nombres.txt` |
| `|` | **Tubería**: la salida de un comando es la entrada del siguiente | `ls | wc -l` |

```bash
$ cat > notas.txt        # escribe texto y termina con Ctrl+D
Primera línea
Segunda línea
$ cat notas.txt
Primera línea
Segunda línea
$ echo "Tercera línea" >> notas.txt
```

## Fichero de práctica

Para los ejemplos usaremos este fichero con datos de alumnos (`nombre:apellido:ciclo:curso:nota`). Créalo copiándolo en un editor o con `cat > alumnos.txt`:

```text title="alumnos.txt"
lucia:garcia:ASIR:1:8
pablo:martinez:SMR:2:5
marta:lopez:ASIR:2:9
jorge:sanchez:DAW:1:4
irene:perez:ASIR:1:7
david:gomez:SMR:1:6
sara:ruiz:DAW:2:8
pablo:navarro:ASIR:2:3
```

## Ver ficheros

### `cat`: mostrar y concatenar

```bash
$ cat alumnos.txt
$ cat fichero1 fichero2 > juntos.txt    # concatena dos ficheros en uno
$ cat -n alumnos.txt                    # numera las líneas
```

### `less`: paginar

Para ficheros largos, `less` permite moverse con las flechas, ++space++ (página siguiente), `/texto` (buscar), ++n++ (siguiente coincidencia) y ++q++ (salir).

```bash
$ less /etc/services
$ sudo less /var/log/syslog
```

### `head` y `tail`: principio y final

Muestran por defecto las **10 primeras** o **10 últimas** líneas. Con `-n` elegimos cuántas:

```bash
$ head -n 3 alumnos.txt
$ tail -n 2 alumnos.txt
```

`tail -f` sigue el fichero en tiempo real, mostrando lo que se va añadiendo. Es imprescindible para ver logs mientras ocurre algo (salimos con ++ctrl+c++):

```bash
$ sudo tail -f /var/log/syslog
```

### `nl`: numerar líneas

```bash
$ nl alumnos.txt
```

### Ver ficheros comprimidos: `zcat`, `bzcat`, `xzcat`

Permiten leer un fichero comprimido sin descomprimirlo, según el algoritmo con el que se comprimió:

| Comando | Formato |
|---|---|
| `zcat` | gzip (`.gz`) |
| `bzcat` | bzip2 (`.bz2`) |
| `xzcat` | xz (`.xz`) |

```bash
$ gzip alumnos.txt          # crea alumnos.txt.gz y borra el original
$ zcat alumnos.txt.gz
$ gunzip alumnos.txt.gz     # lo devuelve a su estado original
```

## Buscar líneas: `grep`

`grep` muestra las líneas que contienen un patrón:

```bash
$ grep ASIR alumnos.txt
$ grep -i asir alumnos.txt     # -i ignora mayúsculas/minúsculas
$ grep -v ASIR alumnos.txt     # -v muestra las que NO lo contienen
$ grep -c ASIR alumnos.txt     # -c cuenta las coincidencias
```

!!! tip "Cuidado con los patrones demasiado cortos"
    `grep 1 alumnos.txt` encuentra cualquier línea con un `1` en cualquier sitio. Afinamos incluyendo el contexto: `grep ':1:' alumnos.txt` busca el `1` entre separadores. En el tema de expresiones regulares veremos patrones mucho más potentes.

## Contar: `wc`

```bash
$ wc alumnos.txt        # líneas, palabras y bytes
$ wc -l alumnos.txt     # solo líneas
$ grep ASIR alumnos.txt | wc -l
```

## Cortar columnas: `cut`

Extrae campos de cada línea. Con `-d` indicamos el **delimitador** y con `-f` los **campos**:

```bash
$ cut -d: -f1 alumnos.txt         # solo los nombres
$ cut -d: -f1,2,5 alumnos.txt     # nombre, apellido y nota
$ cut -d: -f2-4 alumnos.txt       # del campo 2 al 4
$ cut -c1-3 alumnos.txt           # los 3 primeros caracteres
```

## Ordenar: `sort`

```bash
$ sort alumnos.txt                  # orden alfabético
$ sort -r alumnos.txt               # orden inverso
$ sort -t: -k5 -n alumnos.txt       # por el campo 5 (nota), numéricamente
$ sort -t: -k5 -nr alumnos.txt      # de mayor a menor nota
$ sort -R alumnos.txt               # orden aleatorio
$ cut -d: -f3 alumnos.txt | sort -u # ciclos sin repetir
```

## Líneas repetidas: `uniq`

`uniq` elimina (o cuenta) líneas repetidas **consecutivas**. Por eso casi siempre va detrás de `sort`:

```bash
$ cut -d: -f3 alumnos.txt | sort | uniq
ASIR
DAW
SMR
$ cut -d: -f3 alumnos.txt | sort | uniq -c
      4 ASIR
      2 DAW
      2 SMR
```

!!! warning "`uniq` sin `sort`"
    Si las líneas iguales no están juntas, `uniq` no las detecta como repetidas.

## Traducir caracteres: `tr`

`tr` sustituye o elimina caracteres. Solo lee de la entrada estándar, así que siempre lo usamos con tubería o `<`:

```bash
$ tr ':' ',' < alumnos.txt          # cambia : por ,  (crea un CSV)
$ tr 'a-z' 'A-Z' < alumnos.txt      # a mayúsculas
$ echo "hola    mundo" | tr -s ' '  # -s comprime espacios repetidos
$ echo "a1b2c3" | tr -d '0-9'       # -d elimina caracteres
```

Un truco muy útil: la salida de `ls -l` tiene columnas separadas por varios espacios, lo que impide usar `cut` directamente. Con `tr -s` lo arreglamos:

```bash
$ ls -l /etc | tr -s ' ' | cut -d' ' -f3,9    # propietario y nombre
```

## Unir y dividir ficheros: `paste` y `split`

`paste` junta ficheros **línea a línea**, en columnas (por defecto separadas por tabulador):

```bash
$ cut -d: -f1 alumnos.txt > nombres.txt
$ cut -d: -f5 alumnos.txt > notas.txt
$ paste nombres.txt notas.txt
$ paste -d, nombres.txt notas.txt      # separadas por comas
```

`split` divide un fichero grande en trozos:

```bash
$ split -l 3 alumnos.txt parte_       # trozos de 3 líneas: parte_aa, parte_ab...
$ split -l 3 -d alumnos.txt parte_    # con sufijos numéricos: parte_00, parte_01...
$ split -b 10M imagen.iso trozo_      # trozos de 10 MB
```

## Editar texto en flujo: `sed`

`sed` (*stream editor*) transforma el texto línea a línea. Sus usos básicos:

```bash
$ sed -n '/ASIR/p' alumnos.txt       # muestra solo las líneas con ASIR (como grep)
$ sed '/ASIR/d' alumnos.txt          # elimina de la salida las líneas con ASIR
$ sed -n '3p' alumnos.txt            # muestra la línea 3
$ sed -n '2,4p' alumnos.txt          # de la 2 a la 4
$ sed -n '$p' alumnos.txt            # la última línea
$ sed 's/ASIR/Administración/' alumnos.txt     # sustituye la 1.ª aparición de cada línea
$ sed 's/a/A/g' alumnos.txt          # g: sustituye todas las apariciones
```

- `-n` hace que `sed` no muestre nada salvo lo que indiquemos con `p`.
- Sin `-n`, `sed` muestra todo el texto (ya modificado).

Por defecto `sed` **no modifica el fichero**: solo muestra el resultado. Para cambiarlo de verdad usamos `-i`; si añadimos una extensión, guarda antes una copia de seguridad:

```bash
$ sed -i.bak 's/SMR/Sistemas/' alumnos.txt
$ ls alumnos*
alumnos.txt  alumnos.txt.bak
```

## Integridad de ficheros: sumas de comprobación

Una **suma de comprobación** (*hash*) es un valor calculado a partir del contenido de un fichero. Si cambia un solo bit del fichero, el hash cambia por completo. Se usa para comprobar que un fichero descargado o enviado **no se ha corrompido ni manipulado**. Por eso las distribuciones publican junto a sus ISO ficheros como `SHA256SUMS`.

| Comando | Algoritmo |
|---|---|
| `md5sum` | MD5 (antiguo, ya no se considera seguro) |
| `sha256sum` | SHA-256 |
| `sha512sum` | SHA-512 |

```bash
$ sha256sum alumnos.txt
3b1f...e9a2  alumnos.txt
$ sha256sum alumnos.txt > alumnos.sha256     # guardamos el hash
$ sha256sum -c alumnos.sha256                # verificamos
alumnos.txt: OK
$ echo "nueva:linea:ASIR:1:5" >> alumnos.txt
$ sha256sum -c alumnos.sha256
alumnos.txt: FAILED
sha256sum: WARNING: 1 computed checksum did NOT match
```

## Ver el contenido "en bruto": `od`

`od` (*octal dump*) muestra los bytes de un fichero. Es útil para descubrir caracteres invisibles (saltos de línea, tabuladores, retornos de carro de ficheros creados en Windows...):

```bash
$ od -c notas.txt         # como caracteres; \n es salto de línea, \t tabulador
$ od -x notas.txt         # en hexadecimal
$ od -An -c notas.txt     # sin la columna de desplazamiento
```

!!! example "Ficheros de Windows"
    Un fichero de texto creado en Windows termina cada línea con `\r\n`. Con `od -c` verás los `\r`, que a veces hacen fallar los scripts en Linux. Se pueden quitar con `tr -d '\r' < origen > destino`.

## Resumen de comandos

| Comando | Uso |
|---|---|
| `cat` | Mostrar y concatenar ficheros |
| `zcat`, `bzcat`, `xzcat` | Mostrar ficheros comprimidos con gzip, bzip2 y xz |
| `less` | Paginar un fichero, con búsqueda |
| `head` / `tail` | Primeras / últimas líneas (`tail -f` para seguir un fichero) |
| `nl` | Numerar líneas |
| `grep` | Buscar líneas que contienen un patrón |
| `wc` | Contar líneas, palabras y bytes |
| `cut` | Extraer campos o caracteres |
| `sort` | Ordenar |
| `uniq` | Eliminar o contar líneas repetidas consecutivas |
| `tr` | Sustituir, eliminar o comprimir caracteres |
| `paste` | Unir ficheros en columnas |
| `split` | Dividir un fichero en trozos |
| `sed` | Filtrar y transformar texto |
| `md5sum`, `sha256sum`, `sha512sum` | Calcular y verificar sumas de comprobación |
| `od` | Volcar el contenido en octal, hexadecimal o caracteres |

## Ejercicios

Usa el fichero `alumnos.txt` original (si lo modificaste, vuelve a crearlo).

**1.** ¿Cuántos alumnos hay en total? ¿Y cuántos de ASIR?

??? success "Solución"
    ```bash
    $ wc -l alumnos.txt
    $ grep ASIR alumnos.txt | wc -l      # o: grep -c ASIR alumnos.txt
    ```

**2.** Muestra solo el nombre y el apellido de los alumnos de DAW.

??? success "Solución"
    ```bash
    $ grep DAW alumnos.txt | cut -d: -f1,2
    ```

**3.** Muestra los alumnos ordenados de mayor a menor nota y quédate con los tres primeros.

??? success "Solución"
    ```bash
    $ sort -t: -k5 -nr alumnos.txt | head -n 3
    ```

**4.** ¿Cuántos alumnos hay en cada ciclo?

??? success "Solución"
    ```bash
    $ cut -d: -f3 alumnos.txt | sort | uniq -c
    ```

**5.** ¿Qué nombres de pila se repiten?

??? success "Solución"
    ```bash
    $ cut -d: -f1 alumnos.txt | sort | uniq -d
    pablo
    ```
    `uniq -d` muestra solo las líneas que aparecen repetidas.

**6.** Elige al azar un alumno de ASIR para salir a la pizarra (muestra solo su nombre).

??? success "Solución"
    ```bash
    $ grep ASIR alumnos.txt | cut -d: -f1 | sort -R | head -n 1
    ```

**7.** Genera un fichero `alumnos.csv` con el mismo contenido pero separado por comas y con los nombres en mayúsculas.

??? success "Solución"
    ```bash
    $ tr ':' ',' < alumnos.txt | tr 'a-z' 'A-Z' > alumnos.csv
    ```
    Fíjate en que así también se pasan a mayúsculas los apellidos. Para cambiar solo el primer campo haría falta algo más potente (`sed` con expresiones regulares o `awk`).

**8.** Muestra la primera, la cuarta y la última línea del fichero usando **un solo** `sed`.

??? success "Solución"
    ```bash
    $ sed -n -e '1p' -e '4p' -e '$p' alumnos.txt
    ```

**9.** Usando `/etc/passwd`: ¿qué usuarios tienen como shell `/bin/bash`? Muestra solo sus nombres. ¿Cuántos usuarios **no** lo tienen?

??? success "Solución"
    ```bash
    $ grep ':/bin/bash$' /etc/passwd | cut -d: -f1
    $ grep -v ':/bin/bash$' /etc/passwd | wc -l
    ```
    El `$` final indica "al final de la línea" (lo veremos en expresiones regulares).

**10.** ¿Cuántos procesadores (núcleos lógicos) tiene tu máquina? Cada uno aparece en `/proc/cpuinfo` en una línea que empieza por `processor`. Resuélvelo con `grep` y luego con `sed`.

??? success "Solución"
    ```bash
    $ grep processor /proc/cpuinfo | wc -l
    $ sed -n '/processor/p' /proc/cpuinfo | wc -l
    ```
    El comando `nproc` da directamente el mismo dato.

**11.** Calcula la suma SHA-256 de `alumnos.csv` y guárdala en un fichero. Cambia una nota con `sed -i` y comprueba que la verificación falla.

??? success "Solución"
    ```bash
    $ sha256sum alumnos.csv > alumnos.csv.sha256
    $ sha256sum -c alumnos.csv.sha256        # OK
    $ sed -i 's/,4$/,5/' alumnos.csv
    $ sha256sum -c alumnos.csv.sha256        # FAILED
    ```

**12.** Lista el contenido de `/etc` con `ls -l` y muestra solo el propietario y el nombre de los **directorios**.

??? success "Solución"
    ```bash
    $ ls -l /etc | grep '^d' | tr -s ' ' | cut -d' ' -f3,9
    ```
    Las líneas de directorios empiezan por `d`; `^d` significa "empieza por d".
