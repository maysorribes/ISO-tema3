# 3.7 Procesos: crear, supervisar y terminar

Un **proceso** es un programa en ejecución. Cada vez que lanzamos un comando se crea, al menos, un proceso. El kernel identifica a cada uno con un número único, el **PID** (*Process ID*), y sabe también quién lo creó: su proceso padre, el **PPID**.

## Control de trabajos (*jobs*)

Desde una terminal podemos tener varios procesos lanzados a la vez. El shell los llama **trabajos** (*jobs*) y les asigna un número propio, distinto del PID.

### Primer y segundo plano

- En **primer plano** (*foreground*) el proceso ocupa la terminal: no podemos escribir otro comando hasta que termine.
- En **segundo plano** (*background*) el proceso sigue ejecutándose mientras usamos la terminal.

Para lanzar un comando directamente en segundo plano se añade `&` al final:

```bash
$ sleep 300 &
[1] 4521
```

`[1]` es el número de trabajo y `4521` el PID.

### Suspender, reanudar y mover trabajos

| Acción | Cómo |
|---|---|
| Suspender el trabajo en primer plano | ++ctrl+z++ |
| Interrumpir (terminar) el trabajo en primer plano | ++ctrl+c++ |
| Ver los trabajos de esta terminal | `jobs` (`-l` muestra también el PID) |
| Reanudar en segundo plano | `bg %N` |
| Traer a primer plano | `fg %N` |

```bash
$ sleep 500           # se queda bloqueado...
^Z                    # Ctrl+Z
[1]+  Stopped                 sleep 500
$ bg %1               # sigue ejecutándose en segundo plano
[1]+ sleep 500 &
$ jobs -l
[1]+  4602 Running                 sleep 500 &
$ fg %1               # vuelve a primer plano
```

Formas de referirse a un trabajo:

| Especificación | Trabajo |
|---|---|
| `%1`, `%2`... | Por número |
| `%+` o `%%` | El actual (marcado con `+` en `jobs`) |
| `%-` | El anterior (marcado con `-`) |
| `%sleep` | El que empieza por `sleep` |
| `%?500` | El que contiene `500` |

!!! note "Los trabajos son de la terminal"
    `jobs` solo muestra los trabajos de la terminal actual. Si cierras la terminal, el shell envía la señal `SIGHUP` a sus trabajos y normalmente terminan.

## Ver los procesos del sistema

### `ps`: foto instantánea

`ps` muestra los procesos en el momento de ejecutarlo. Por razones históricas acepta tres estilos de opciones:

| Estilo | Ejemplo | Rasgo |
|---|---|---|
| UNIX (System V) | `ps -ef` | Opciones con guion |
| BSD | `ps aux` | Opciones sin guion |
| GNU | `ps --forest` | Opciones largas con dos guiones |

Las combinaciones más usadas:

```bash
$ ps                          # procesos de esta terminal
$ ps aux                      # todos los procesos, con usuario, %CPU y %MEM
$ ps -ef                      # todos, con PID y PPID
$ ps -ef --forest             # en árbol (también: pstree)
$ ps -u alumno                # los de un usuario
$ ps -o pid,ppid,user,%cpu,%mem,cmd   # elegir columnas
$ ps aux --sort=-%mem | head          # los que más memoria usan
```

Columnas de `ps aux`:

| Columna | Significado |
|---|---|
| `USER` | Propietario |
| `PID` | Identificador |
| `%CPU` / `%MEM` | Uso de procesador y memoria |
| `VSZ` / `RSS` | Memoria virtual / memoria física real (KiB) |
| `TTY` | Terminal (`?` si no tiene) |
| `STAT` | Estado |
| `START` / `TIME` | Hora de inicio / tiempo de CPU consumido |
| `COMMAND` | Comando |

Estados más habituales (`STAT`):

| Estado | Significado |
|---|---|
| `R` | En ejecución o listo para ejecutarse |
| `S` | Dormido, esperando un evento (la mayoría) |
| `D` | Esperando entrada/salida; no se puede interrumpir |
| `T` | Detenido (por ejemplo con ++ctrl+z++) |
| `Z` | Zombi: ha terminado, pero su padre aún no ha recogido su estado |

### `top`: monitor en tiempo real

`top` muestra los procesos actualizándose cada pocos segundos. La parte superior resume el estado del sistema: tiempo encendido, usuarios, **carga media**, tareas por estado, uso de CPU y memoria.

Teclas útiles dentro de `top`:

| Tecla | Acción |
|---|---|
| ++shift+p++ | Ordenar por CPU (por defecto) |
| ++shift+m++ | Ordenar por memoria |
| ++shift+t++ | Ordenar por tiempo de CPU |
| ++shift+n++ | Ordenar por PID |
| ++c++ | Mostrar la ruta completa del comando |
| ++u++ | Filtrar por usuario |
| ++k++ | Enviar una señal (matar) a un PID |
| ++r++ | Cambiar la prioridad (*renice*) de un PID |
| ++1++ | Ver cada CPU por separado |
| ++q++ | Salir |

`htop` es una alternativa más visual (hay que instalarla).

### Otras herramientas

```bash
$ uptime            # tiempo encendido, usuarios y carga media (1, 5 y 15 min)
$ free -h           # memoria y swap
$ pgrep sshd        # PID de los procesos cuyo nombre coincide
$ pgrep -u root -l ssh
$ pidof sshd        # PID de un programa por su nombre exacto
$ watch -n 2 free -h    # repite un comando cada 2 segundos (Ctrl+C para salir)
```

!!! info "Carga media"
    La carga media indica cuántos procesos, de promedio, estaban ejecutándose o esperando CPU. Se interpreta según el número de núcleos: con 4 núcleos, una carga de 4 significa que están todos ocupados.

## Señales

Para comunicarse con un proceso le enviamos **señales**. Cada una tiene un número y un nombre:

| Nº | Nombre | Efecto habitual |
|---|---|---|
| 1 | `SIGHUP` | "Cuelgue". Muchos servicios la usan para **releer su configuración** |
| 2 | `SIGINT` | Interrupción (lo que envía ++ctrl+c++) |
| 9 | `SIGKILL` | Terminación inmediata. **No se puede capturar ni ignorar** |
| 15 | `SIGTERM` | Petición de terminar ordenadamente. **Es la señal por defecto** |
| 18 | `SIGCONT` | Continuar un proceso detenido |
| 19 | `SIGSTOP` | Detener (no se puede ignorar) |
| 20 | `SIGTSTP` | Detener desde terminal (lo que envía ++ctrl+z++) |

`kill -l` muestra la lista completa.

### Enviar señales

```bash
$ kill 4521              # envía SIGTERM al PID 4521
$ kill -15 4521          # igual, por número
$ kill -SIGTERM 4521     # igual, por nombre
$ kill -TERM 4521        # igual, sin el prefijo SIG
$ kill -9 4521           # SIGKILL: último recurso
$ kill %1                # también funciona con trabajos
$ kill -HUP $(pidof nginx)   # recargar la configuración de un servicio
```

Por nombre en lugar de PID:

```bash
$ pkill sleep            # señal a los procesos cuyo nombre contiene "sleep"
$ pkill -u alumno        # a todos los procesos de un usuario
$ killall sleep          # a todos los procesos llamados exactamente "sleep"
```

!!! warning "Primero `SIGTERM`, luego `SIGKILL`"
    `SIGTERM` deja que el programa cierre ficheros y libere recursos. `SIGKILL` lo corta en seco y puede dejar datos corruptos o ficheros temporales. Úsala solo si el proceso no responde.

## Resumen de comandos

| Comando | Uso |
|---|---|
| `&` | Lanzar en segundo plano |
| `jobs`, `fg`, `bg` | Gestionar trabajos de la terminal |
| `ps` | Listar procesos |
| `top` / `htop` | Monitor de procesos en tiempo real |
| `uptime`, `free` | Carga y memoria del sistema |
| `watch` | Repetir un comando periódicamente |
| `pgrep`, `pidof` | Obtener el PID por nombre |
| `kill` | Enviar una señal por PID o trabajo |
| `pkill`, `killall` | Enviar una señal por nombre |

## Ejercicios

**1.** Lanza `sleep 600` en primer plano, suspéndelo, reanúdalo en segundo plano y comprueba con `jobs -l` su estado y su PID.

??? success "Solución"
    ```bash
    $ sleep 600
    ^Z
    $ bg %1
    $ jobs -l
    ```

**2.** Lanza tres `sleep` en segundo plano (`sleep 1000 &`, `sleep 2000 &`, `sleep 3000 &`). Trae a primer plano el de `2000` usando su contenido y termínalo con ++ctrl+c++.

??? success "Solución"
    ```bash
    $ fg %?2000
    ^C
    ```

**3.** Termina el resto de trabajos `sleep` con una sola orden por nombre.

??? success "Solución"
    ```bash
    $ pkill sleep        # o: killall sleep
    ```

**4.** Muestra todos los procesos del sistema en forma de árbol. ¿Cuál es el PID 1 y qué proceso es?

??? success "Solución"
    ```bash
    $ ps -ef --forest     # o: pstree -p
    $ ps -p 1
    ```
    El PID 1 es el primer proceso que arranca el kernel; en las distribuciones actuales es `systemd`. Es el antepasado de todos los demás.

**5.** Muestra solo el PID, el usuario, el % de memoria y el comando de los 5 procesos que más memoria consumen.

??? success "Solución"
    ```bash
    $ ps -eo pid,user,%mem,cmd --sort=-%mem | head -n 6
    ```
    Son 6 líneas porque la primera es la cabecera.

**6.** Abre `top`, ordena por memoria, filtra los procesos de tu usuario y sal.

??? success "Solución"
    Dentro de `top`: ++shift+m++, después ++u++, tu nombre de usuario y ++enter++; para salir, ++q++.

**7.** ¿Cuál es la carga media del sistema? ¿Cuántos núcleos tiene? ¿Está muy cargado?

??? success "Solución"
    ```bash
    $ uptime
    $ nproc
    ```
    Si la carga media es claramente inferior al número de núcleos, el sistema va holgado.

**8.** Con `watch`, muestra cada segundo el número de procesos que hay en el sistema.

??? success "Solución"
    ```bash
    $ watch -n 1 'ps -e | wc -l'
    ```
    Las comillas hacen que la tubería la ejecute `watch` y no el shell una sola vez.

**9.** Si tienes un servidor web instalado (`apache2` o `nginx`), averigua los PID de sus procesos y haz que recargue la configuración enviando la señal adecuada.

??? success "Solución"
    ```bash
    $ pidof nginx                       # o pgrep apache2
    $ sudo pkill -HUP nginx             # o: sudo kill -HUP <PID del proceso maestro>
    ```
    En sistemas con systemd lo habitual es `sudo systemctl reload nginx`, que hace lo mismo por debajo.
