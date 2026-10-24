# Práctica 7 · Enlaces y jerarquía de directorios

[Descargar el enunciado en PDF](pdf/UT3_P7_Enlaces_FHS.pdf){ .md-button .md-button--primary }

| | |
|---|---|
| **Apartados de los apuntes** | 3.15 Enlaces duros y simbólicos · 3.16 Jerarquía de directorios |
| **Entorno** | Máquina virtual Ubuntu y una memoria USB (o un segundo disco virtual) |
| **Entrega** | `UT3_P7_Apellido_Nombre.pdf` |

## Objetivo

Comprender la relación entre nombres de fichero, inodos y enlaces; saber dónde guarda Linux cada tipo de información según el FHS; y localizar ficheros y comandos con distintas herramientas.

## Qué hay que entregar

Una memoria en PDF con, para cada ejercicio, el **comando** (como texto), una **captura** del resultado con tu *prompt* y la **respuesta razonada** a las preguntas. Trabaja dentro de `~/PRACTICA7`.

## Parte A · Enlaces duros

1. Crea el fichero `informe.txt` con tres líneas de texto. Muestra su número de inodo y su contador de enlaces.
2. Crea dos enlaces duros a `informe.txt`, uno en `PRACTICA7` llamado `informe_bis.txt` y otro en tu directorio personal llamado `informe_home.txt`. Muestra los tres con su inodo. ¿Cuánto vale ahora el contador?
3. Añade una línea a `informe_home.txt` y muestra el contenido de `informe.txt`. Explica el resultado.
4. Haz una **copia** con `cp` de `informe.txt` llamada `informe_copia.txt`. Compara su inodo con el de los demás. Modifica la copia: ¿cambia el original?
5. Borra `informe.txt`. ¿Siguen disponibles los datos? ¿Qué ha pasado con el contador de enlaces? ¿Cuándo se liberarán de verdad los datos del disco?

## Parte B · Enlaces simbólicos

6. Crea en tu directorio personal un enlace simbólico llamado `logs` que apunte a `/var/log`. Entra en él y muestra la ruta en la que estás de dos formas: la "lógica" y la física.
7. Crea en `PRACTICA7` un enlace simbólico `ultimo` a `informe_bis.txt`. Muestra con `ls -li` los dos ficheros y explica las diferencias de inodo, tipo, permisos y tamaño.
8. Renombra `informe_bis.txt` a `informe_final.txt`. ¿Qué pasa con `ultimo`? Arréglalo **sin** borrarlo antes.
9. Crea el directorio `PRACTICA7/sub` y, estando en `PRACTICA7`, crea dentro de `sub` un enlace simbólico a `informe_final.txt` usando una **ruta relativa**. Comprueba si funciona. Si no funciona, explica por qué y créalo bien.
10. Mueve el enlace del ejercicio anterior a tu directorio personal. ¿Sigue funcionando? ¿Habría funcionado con una ruta absoluta?

## Parte C · Límites de los enlaces

11. Intenta crear un enlace duro al directorio `PRACTICA7/sub`. ¿Qué mensaje obtienes?
12. Conecta una memoria USB a la máquina virtual (o añade un segundo disco) y averigua dónde se ha montado. Intenta crear en ella un enlace **duro** a `informe_final.txt`. Después crea un enlace **simbólico**. Explica por qué uno funciona y el otro no.
13. Busca todos los enlaces simbólicos **rotos** de tu directorio personal y bórralos con una sola orden.

## Parte D · Jerarquía de directorios

14. Muestra el contenido del directorio raíz con `ls -l`. Para **cada** directorio, explica en una línea qué contiene según el FHS. Indica también cuáles son enlaces simbólicos y a dónde apuntan.
15. Indica en qué directorio buscarías cada uno de estos elementos y demuestra que está ahí:

    a) El fichero de configuración de la red (`netplan`).
    b) El registro de arranque del sistema o el de autenticación.
    c) El kernel con el que ha arrancado la máquina.
    d) La lista de particiones que se montan al arrancar.
    e) La documentación instalada del paquete `bash`.
    f) Los paquetes `.deb` descargados por `apt`.
    g) El dispositivo que corresponde a tu disco duro.

16. Muestra cuánto ocupa cada directorio de la raíz y ordénalos de menor a mayor. ¿Por qué `/proc` y `/sys` aparecen con 0?
17. Usando **solo ficheros de `/proc`**, averigua el modelo de tu procesador, la memoria total y la versión del kernel.

## Parte E · Localizar ficheros y comandos

18. Instala `plocate` y actualiza su base de datos. Busca todos los ficheros cuyo nombre sea exactamente `fstab`.
19. Crea el fichero `~/PRACTICA7/localizame_TUUSUARIO.txt` y búscalo con `locate`. ¿Lo encuentra? ¿Qué tienes que hacer para que aparezca?
20. Para el comando `ls`, el comando `cd` y el comando `passwd`, averigua con `which`, `whereis` y `type`:

    a) Dónde está el ejecutable (si lo hay).
    b) Dónde está su página de manual.
    c) Si es un programa, un comando interno del shell o un alias.

!!! question "Pregunta final"
    En las distribuciones actuales, `/bin` es un enlace simbólico a `/usr/bin`. ¿Qué ventaja tiene esto? ¿Por qué no podría ser un enlace **duro**?
