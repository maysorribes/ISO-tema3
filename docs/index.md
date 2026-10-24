# Tema 3 · Configuración básica de Linux

El tema tiene dos partes. En la **Parte 1** aprenderemos a trabajar con soltura en la **línea de comandos de Linux**: cómo funciona el entorno del shell, cómo procesar texto con filtros, cómo crear, buscar y archivar ficheros, y cómo gestionar procesos. En la **Parte 2** veremos la **administración básica**: usuarios y grupos, permisos, enlaces y la organización del sistema de archivos.

Todo lo que veremos se puede practicar en cualquier distribución (Ubuntu, Debian, Rocky, etc.), en una máquina virtual o en un contenedor.

## Contenidos

### Parte 1 · Línea de comandos

| Apartado | Contenido | Objetivo LPIC-1 |
|---|---|---|
| [3.1 Variables y caracteres especiales](103-1-variables.md) | Variables de entorno, `echo`, `env`, `set`, `export`, `unset`, comillas y escape | 103.1 |
| [3.2 Filtros de texto](103-2-filtros.md) | Redirecciones y tuberías, `cat`, `less`, `head`, `tail`, `grep`, `sed`, `cut`, `sort`, `uniq`, `wc`, `tr`, `paste`, `split`, sumas de comprobación, `od` | 103.2 |
| [3.3 Gestión básica de archivos](103-3-archivos.md) | `ls`, `touch`, `cp`, `mv`, `rm`, `mkdir`, `rmdir`, recursividad y comodines | 103.3 |
| [3.4 Búsqueda, archivado y copia](103-3-find-tar.md) | `find`, `tar`, `gzip`, `bzip2`, `cpio`, `dd` | 103.3 |
| [3.5 Redirecciones](103-4-redirecciones.md) | Descriptores, `>`, `>>`, `2>`, `&>`, `2>&1`, `/dev/null`, `<`, *here documents* y *here strings* | 103.4 |
| [3.6 Tuberías, tee y xargs](103-4-tuberias.md) | Tuberías, `tee`, sustitución de comandos `$( )`, `xargs` | 103.4 |
| [3.7 Procesos](103-5-procesos.md) | Trabajos (`jobs`, `fg`, `bg`), `ps`, `top`, señales, `kill`, `pkill`, `killall` | 103.5 |
| [3.8 Prioridad de procesos](103-6-prioridades.md) | Valor *nice*, `nice`, `renice`, prioridades en `ps` y `top` | 103.6 |
| [3.9 Expresiones regulares](103-7-regex.md) | Anclas, listas, clases POSIX, cuantificadores, grupos, alternativas, BRE y ERE | 103.7 |
| [3.10 grep y sed](103-7-grep-sed.md) | Opciones avanzadas de `grep`, direcciones e instrucciones de `sed`, sustituciones con grupos | 103.7 |

### Parte 2 · Usuarios y sistema de archivos

| Apartado | Contenido | Objetivo LPIC-1 |
|---|---|---|
| [3.11 Gestión de usuarios y grupos](107-1-usuarios.md) | `useradd`, `usermod`, `userdel`, `groupadd`, `gpasswd`, `passwd`, `chage`, `/etc/skel`, `su` y `sudo` | 107.1 |
| [3.12 Ficheros de cuentas](107-1-ficheros-cuentas.md) | `/etc/passwd`, `/etc/shadow`, `/etc/group`, `/etc/gshadow`, `/etc/login.defs`, `getent` | 107.1 |
| [3.13 Permisos y propietarios](104-5-permisos.md) | `rwx`, `chmod` simbólico y octal, `chown`, `chgrp`, `umask` | 104.5 |
| [3.14 Permisos especiales](104-5-permisos-especiales.md) | SUID, SGID y *sticky bit*: qué hacen, cómo se ven y cómo se asignan | 104.5 |
| [3.15 Enlaces duros y simbólicos](104-6-enlaces.md) | Inodos, `ln`, `ln -s`, enlaces rotos, rutas relativas y absolutas | 104.6 |
| [3.16 Jerarquía de directorios](104-7-fhs.md) | FHS, `find`, `locate`, `updatedb`, `which`, `whereis`, `type` | 104.7 |

## Prácticas

A lo largo del tema harás y entregarás **ocho prácticas**. En la sección [Prácticas](practicas/index.md) tienes el calendario, las normas de entrega y los enunciados para descargar.


## Cómo usar estos apuntes

- Los bloques de código que empiezan por `$` son comandos para escribir en la terminal; **no copies el `$`**.
- Cada apartado termina con **ejercicios**. La solución está plegada: intenta resolverlo antes de abrirla.
- Para ver todas las opciones de un comando usa siempre el manual: `man comando` (sal con ++q++).

!!! info "Referencia"
    Estos apuntes siguen el temario de los objetivos 103, 104 y 107 de la certificación **LPIC-1** del Linux Professional Institute. Puedes ampliar en los [materiales oficiales de LPI](https://learning.lpi.org/es/learning-materials/).
