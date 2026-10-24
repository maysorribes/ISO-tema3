# 3.8 Prioridad de los procesos

En un sistema hay muchos más procesos que núcleos de CPU. El **planificador** (*scheduler*) del kernel reparte el tiempo de procesador entre ellos, cambiando de uno a otro muchas veces por segundo. Nosotros podemos influir en ese reparto indicando qué procesos son más o menos importantes.

## Prioridad y valor *nice*

Linux distingue dos grandes tipos de procesos:

- **Procesos normales**: la inmensa mayoría (lo que lanzan los usuarios y casi todos los servicios).
- **Procesos de tiempo real**: necesitan responder en plazos muy estrictos (audio profesional, control industrial). Siempre pasan por delante de los normales.

En los procesos normales, la prioridad que podemos ajustar es el **valor *nice*** ("amable"):

| Valor *nice* | Significado |
|---|---|
| `-20` | Prioridad **máxima** (el proceso es "poco amable": acapara CPU) |
| `0` | Valor por defecto |
| `19` | Prioridad **mínima** (el proceso "cede" la CPU a los demás) |

!!! tip "Para recordarlo"
    Cuanto **más alto** es el *nice*, más amable es el proceso con los demás y **menos** CPU se lleva.

Solo importa cuando hay **competencia** por la CPU: si el sistema está desocupado, un proceso con *nice* 19 se ejecutará igual de rápido que uno con 0.

### Quién puede cambiarlo

| Acción | Usuario normal | `root` |
|---|---|---|
| Aumentar el *nice* (bajar prioridad) | Sí, en sus procesos | Sí |
| Disminuir el *nice* (subir prioridad) | **No** | Sí |
| Usar valores negativos | **No** | Sí |

## Ver la prioridad

En `ps` y `top` aparecen dos columnas relacionadas:

- **`NI`**: el valor *nice*.
- **`PRI`** o **`PR`**: la prioridad que usa el kernel, calculada a partir del *nice*. En `top`, para procesos normales, `PR = 20 + NI` (de 0 a 39); los de tiempo real aparecen como `rt`.

```bash
$ ps -l                        # procesos de la terminal con columnas PRI y NI
$ ps -eo pid,ni,pri,cmd        # todos, eligiendo columnas
$ ps -o pid,ni,cmd -p 1234     # un proceso concreto
```

En `top`, las columnas `PR` y `NI` se ven directamente.

## Lanzar un proceso con otra prioridad: `nice`

```bash
$ nice tar -czf copia.tar.gz /home         # nice sin opciones: +10
$ nice -n 15 ./calculo_largo.sh            # con nice 15
$ sudo nice -n -5 ./servicio_critico       # negativo: solo root
```

!!! note "Sintaxis antigua"
    También verás `nice -15 comando`, que significa *nice* **+15** (el guion es el de la opción, no un signo negativo). Para un valor negativo con esa sintaxis se escribe `nice --5`. Es fácil confundirse, así que mejor usa siempre `-n`.

## Cambiar la prioridad de un proceso en marcha: `renice`

```bash
$ renice -n 10 -p 1234          # el PID 1234 pasa a nice 10
$ renice -n 5 -u alumno         # todos los procesos del usuario alumno
$ renice -n 19 -g profesores    # todos los del grupo profesores
$ sudo renice -n -10 -p 1234    # subir prioridad: solo root
```

Desde `top` también se puede: tecla ++r++, el PID y el nuevo valor.

## Casos de uso

- **Copias de seguridad, compresiones o compilaciones largas** en un servidor que da servicio: se lanzan con `nice -n 19` para que no ralenticen a los usuarios.
- **Un proceso que se ha "desbocado"** y acapara la CPU: en lugar de matarlo, podemos bajarle la prioridad con `renice` mientras investigamos.
- **Un servicio crítico**: el administrador puede darle un *nice* negativo.

## Resumen

| Comando | Uso |
|---|---|
| `nice -n N comando` | Ejecutar con *nice* N (sin `-n`: +10) |
| `renice -n N -p PID` | Cambiar el *nice* de un proceso en marcha |
| `renice -n N -u usuario` | ... de todos los procesos de un usuario |
| `ps -l`, `ps -o ni,pri` | Ver *nice* y prioridad |
| `top` (columnas `PR`, `NI`; tecla ++r++) | Ver y cambiar prioridades en vivo |

## Ejercicios

**1.** Muestra el PID, el valor *nice* y el comando de todos los procesos, ordenados por *nice* de menor a mayor. ¿Hay alguno con *nice* negativo? ¿De quién es?

??? success "Solución"
    ```bash
    $ ps -eo pid,ni,user,cmd --sort=ni | head -n 15
    ```
    Suelen aparecer procesos del kernel y algunos servicios del sistema, todos de `root`.

**2.** Lanza `sleep 1000` en segundo plano con la prioridad mínima y comprueba su valor *nice* con `ps`.

??? success "Solución"
    ```bash
    $ nice -n 19 sleep 1000 &
    $ ps -o pid,ni,cmd -p $!
    ```
    `$!` contiene el PID del último proceso lanzado en segundo plano.

**3.** Lanza `sleep 2000 &` sin `nice`. Con tu usuario normal, súbele el *nice* a 5 y después intenta bajarlo a 0. ¿Qué pasa?

??? success "Solución"
    ```bash
    $ sleep 2000 &
    $ renice -n 5 -p $!
    $ renice -n 0 -p $!
    renice: failed to set priority for ...: Permission denied
    ```
    Un usuario normal solo puede bajar la prioridad (subir el *nice*) de sus procesos, nunca subirla.

**4.** Repite el último `renice` con `sudo`. ¿Funciona ahora? Ponle después *nice* `-5`.

??? success "Solución"
    ```bash
    $ sudo renice -n 0 -p <PID>
    $ sudo renice -n -5 -p <PID>
    ```
    Sí: `root` puede asignar cualquier valor entre -20 y 19.

**5.** ¿Qué valor *nice* tendrá el proceso en cada caso?

- a) `nice sleep 100 &`
- b) `nice -n 3 sleep 100 &`
- c) `nice -7 sleep 100 &`
- d) `sudo nice --7 sleep 100 &`

??? success "Solución"
    a) 10 · b) 3 · c) 7 · d) -7

**6.** Comprueba el efecto real de la prioridad. Lanza en segundo plano, en una máquina con pocos núcleos, varias copias de un bucle infinito: unas con *nice* 0 y otras con 19. Observa en `top` el `%CPU` de cada una. Mátalas al terminar.

```bash
$ for i in $(seq $(nproc)); do (while :; do :; done) & done
$ for i in $(seq $(nproc)); do nice -n 19 bash -c 'while :; do :; done' & done
```

??? success "Solución"
    En `top` las copias con *nice* 0 se reparten casi toda la CPU y las de *nice* 19 apenas reciben tiempo. Para terminarlas: `kill $(jobs -p)`.

**7.** Baja con `renice` la prioridad de **todos** los procesos de tu usuario a *nice* 2. ¿Afecta a los procesos que lances después?

??? success "Solución"
    ```bash
    $ renice -n 2 -u $USER
    ```
    Afecta a los procesos existentes. Los que lance después ese mismo shell heredan su *nice* (2), porque el valor se hereda del proceso padre; los de una terminal nueva empezarán en 0.
