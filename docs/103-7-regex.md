# 3.9 Expresiones regulares

Una **expresión regular** (*regex*) es un patrón que describe un conjunto de cadenas de texto. Sirve para buscar, validar o transformar texto: "líneas que empiezan por `#`", "cualquier dirección IP", "palabras de cinco letras acabadas en *ción*"...

Las usan muchas herramientas: `grep`, `sed`, `awk`, `less`, `vim`, y casi todos los lenguajes de programación.

!!! warning "No confundir con los comodines"
    Los comodines del shell (`*`, `?`, `[ ]`) se parecen, pero **no son lo mismo**. En un comodín `*` significa "cualquier cosa"; en una expresión regular significa "el elemento anterior repetido cero o más veces". Los comodines sirven para **nombres de ficheros**; las expresiones regulares, para **contenido de texto**.

Para practicar usaremos `grep` y este fichero:

```text title="regex.txt"
Ana Garcia 600123456 ana.garcia@iesmail.es
luis perez 961234567 luis@correo.com
Marta Lopez 655 11 22 33 marta.lopez@iesmail.es
# esto es un comentario
pedro gomez 34600999888
color
colour
192.168.1.10
10.0.0.300
```

## Expresiones regulares básicas y extendidas

Hay dos "dialectos" POSIX:

- **Básicas (BRE)**: las que usan por defecto `grep` y `sed`. Algunos metacaracteres (`?`, `+`, `{ }`, `|`, `( )`) hay que escribirlos con barra invertida para que tengan significado especial.
- **Extendidas (ERE)**: se activan con `grep -E` (o `egrep`) y `sed -E` (o `sed -r`). Los metacaracteres funcionan **sin** barra.

En este apartado usaremos casi siempre **extendidas** (`grep -E`), que son más legibles.

## Caracteres literales y el punto

Una letra o número coincide consigo mismo. El **punto** `.` coincide con **cualquier carácter** (uno solo):

```bash
$ grep 'iesmail' regex.txt       # literal
$ grep 'col.r' regex.txt         # color... y también colXr, col3r
```

Para buscar un punto literal hay que **escaparlo** con `\`:

```bash
$ grep 'iesmail\.es' regex.txt
```

## Anclas: inicio y final

| Ancla | Significado |
|---|---|
| `^` | Inicio de línea |
| `$` | Final de línea |
| `\b` | Límite de palabra (extensión de GNU) |
| `\<` / `\>` | Inicio / final de palabra (GNU) |

```bash
$ grep '^#' regex.txt            # líneas que empiezan por #
$ grep -v '^#' regex.txt         # las que no son comentarios
$ grep 'es$' regex.txt           # acaban en "es"
$ grep '^$' fichero              # líneas vacías
$ grep -v '^$' fichero           # quitar líneas vacías
$ grep '\bana\b' regex.txt       # la palabra "ana" completa
```

## Listas de caracteres: `[ ]`

Entre corchetes se pone un **conjunto** de caracteres; coincide con **uno** de ellos:

| Expresión | Coincide con |
|---|---|
| `[aeiou]` | Una vocal minúscula |
| `[0-9]` | Un dígito |
| `[a-zA-Z]` | Una letra sin acentos |
| `[^0-9]` | Cualquier carácter que **no** sea un dígito (`^` al principio niega) |
| `[.-]` | Un punto o un guion (dentro de corchetes el punto es literal) |

```bash
$ grep '^[A-Z]' regex.txt        # líneas que empiezan por mayúscula
$ grep '^[^#]' regex.txt         # líneas que no empiezan por #
```

### Clases POSIX

Son conjuntos predefinidos que funcionan **dentro** de unos corchetes (de ahí los dobles corchetes). Tienen la ventaja de respetar el idioma (por ejemplo, incluyen la `ñ` y las vocales con tilde):

| Clase | Equivale a |
|---|---|
| `[[:digit:]]` | `[0-9]` |
| `[[:alpha:]]` | Letras |
| `[[:alnum:]]` | Letras y dígitos |
| `[[:upper:]]` / `[[:lower:]]` | Mayúsculas / minúsculas |
| `[[:space:]]` | Espacio, tabulador, salto de línea... |
| `[[:punct:]]` | Signos de puntuación |

```bash
$ grep '[[:digit:]]' regex.txt         # líneas con algún dígito
$ grep '^[[:upper:]]' regex.txt
```

## Cuantificadores: cuántas veces

Se colocan **detrás** del elemento al que afectan:

| Cuantificador (ERE) | En BRE | Significado |
|---|---|---|
| `*` | `*` | 0 o más veces |
| `+` | `\+` | 1 o más veces |
| `?` | `\?` | 0 o 1 vez (opcional) |
| `{n}` | `\{n\}` | Exactamente n veces |
| `{n,}` | `\{n,\}` | Al menos n veces |
| `{n,m}` | `\{n,m\}` | Entre n y m veces |

```bash
$ grep -E 'colou?r' regex.txt              # color y colour
$ grep -E '[0-9]{9}' regex.txt             # nueve dígitos seguidos
$ grep -E '^[0-9]+$' fichero               # líneas que solo tienen dígitos
$ grep -E '6[0-9]{8}' regex.txt            # un móvil que empieza por 6
$ grep '[0-9]\{9\}' regex.txt              # lo mismo en BRE
```

La combinación `.*` significa "cualquier cosa, de cualquier longitud":

```bash
$ grep -E '^Ana.*es$' regex.txt            # empieza por Ana y acaba en es
```

## Grupos y alternativas

- Los **paréntesis** `( )` agrupan una parte para aplicarle un cuantificador o para reutilizarla.
- La **barra vertical** `|` indica alternativa: "esto **o** aquello".

```bash
$ grep -E 'perez|gomez' regex.txt          # una u otra
$ grep -E '^(Ana|Marta) ' regex.txt
$ grep -E '([0-9]{1,3}\.){3}[0-9]{1,3}' regex.txt   # aspecto de IPv4
```

En BRE se escriben `\( \)` y `\|`.

!!! note "Coincidir con la forma no es validar"
    El último patrón encuentra `10.0.0.300`, que **no** es una IP válida (300 > 255). Las expresiones regulares describen **forma**, no significado. Validar una IP con exactitud requiere un patrón mucho más largo.

## Referencias inversas

Lo que coincide dentro de un grupo `( )` se puede volver a usar con `\1`, `\2`... (el primer grupo, el segundo...):

```bash
$ grep -E '(.)\1' regex.txt          # algún carácter repetido seguido: "ll", "00"...
$ grep -E '\b(\w+) \1\b' texto.txt   # palabras repetidas: "el el", "de de"
```

Donde realmente brillan es en las sustituciones con `sed` (apartado siguiente).

## Resumen de metacaracteres

| Metacarácter | Significado |
|---|---|
| `.` | Un carácter cualquiera |
| `^` / `$` | Inicio / final de línea |
| `[abc]` / `[^abc]` | Uno de la lista / uno que no esté |
| `[[:clase:]]` | Clase POSIX (`digit`, `alpha`, `upper`...) |
| `*` `+` `?` | 0 o más / 1 o más / 0 o 1 |
| `{n,m}` | Entre n y m repeticiones |
| `( )` | Grupo |
| `|` | Alternativa |
| `\1` | Referencia al primer grupo |
| `\` | Escapa un metacarácter (`\.`, `\$`, `\*`) |

## Ejercicios

Usa el fichero `regex.txt`.

**1.** Muestra las líneas que **no** sean comentarios ni estén vacías.

??? success "Solución"
    ```bash
    $ grep -Ev '^#|^$' regex.txt
    ```

**2.** Muestra las líneas que empiezan por minúscula.

??? success "Solución"
    ```bash
    $ grep '^[a-z]' regex.txt        # o: grep '^[[:lower:]]' regex.txt
    ```

**3.** Muestra las líneas que contienen un número de teléfono de 9 dígitos **seguidos**.

??? success "Solución"
    ```bash
    $ grep -E '[0-9]{9}' regex.txt
    ```
    Fíjate en que también aparece `34600999888` (11 dígitos), porque contiene 9 seguidos. Para exigir exactamente 9: `grep -E '\b[0-9]{9}\b' regex.txt`.

**4.** Busca `color` y `colour` con **una** expresión regular, primero extendida y después básica.

??? success "Solución"
    ```bash
    $ grep -E 'colou?r' regex.txt
    $ grep 'colou\?r' regex.txt
    ```

**5.** Muestra solo las direcciones de correo del dominio `iesmail.es` (usa `-o`, que muestra solo la parte que coincide).

??? success "Solución"
    ```bash
    $ grep -Eo '[[:alnum:]._]+@iesmail\.es' regex.txt
    ```

**6.** Extrae todas las direcciones de correo, sea cual sea el dominio.

??? success "Solución"
    ```bash
    $ grep -Eo '[[:alnum:]._-]+@[[:alnum:].-]+\.[[:alpha:]]{2,}' regex.txt
    ```

**7.** Muestra las líneas que tienen aspecto de dirección IPv4. ¿Hay alguna que no sea válida?

??? success "Solución"
    ```bash
    $ grep -E '^([0-9]{1,3}\.){3}[0-9]{1,3}$' regex.txt
    ```
    `10.0.0.300` encaja con el patrón, pero no es válida porque el último octeto supera 255.

**8.** En `/etc/passwd`, muestra los usuarios cuyo UID (tercer campo) tenga 4 cifras.

??? success "Solución"
    ```bash
    $ grep -E '^[^:]+:[^:]*:[0-9]{4}:' /etc/passwd
    ```
    `[^:]+` significa "uno o más caracteres que no sean dos puntos", es decir, un campo completo.

**9.** Muestra las líneas de `/etc/services` que se refieren a los puertos 22, 80 o 443 por TCP.

??? success "Solución"
    ```bash
    $ grep -E '[[:space:]](22|80|443)/tcp' /etc/services
    ```

**10.** ¿Con cuáles de estas cadenas coincide `^a.c$`? `abc`, `ac`, `a.c`, `abbc`, `aXc`.

??? success "Solución"
    Con `abc`, `a.c` y `aXc`: debe haber exactamente un carácter (cualquiera) entre la `a` y la `c`.
