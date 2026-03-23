---
title: "UD3 — Planes de ejecución Spark en el aula"
author: "José Manuel Sánchez Álvarez"
institution: "IES Rafael Alberti"
course: "Sistemas de Big Data · 2025–2026"
revealjs-theme: simple
revealjs-transition: slide
---

## Antes de empezar el laboratorio

### ⚠️ Importante sobre la infraestructura

Hoy **no todos vais a trabajar exactamente igual**,  
y eso **no es un problema**.

Lo importante es:
👉 **entender Spark y el modelo distribuido**

---

## Tres formas válidas de trabajar con Spark

Dependiendo de la red y del equipo, usaremos:

- **Plan A** — Clúster real (varias máquinas)
- **Plan B** — Clúster en una sola máquina
- **Plan C** — Spark local

El **código es el mismo** en todos los casos.

---

## 🅰️ Plan A — Clúster real (ideal)

### ¿En qué consiste?
- Un alumno actúa como **Spark Master**
- Otros alumnos se conectan como **Workers**
- Cada uno desde su propio portátil

### Qué demuestra
- Arquitectura real de clúster
- Procesos distribuidos
- Comunicación entre nodos

---

## Plan A — Cuándo usarlo

✔ La red permite conexión entre portátiles  
✔ Todos estáis en la misma LAN  
✔ No hay aislamiento WiFi  

👉 **Es la situación ideal**

---

## 🅱️ Plan B — Clúster en una sola máquina (recomendado)

### ¿En qué consiste?
- Master y Worker en el **mismo portátil**
- Contenedores distintos
- Comunicación real entre procesos

### Qué demuestra
- El modelo Master / Worker
- Spark sigue siendo distribuido
- Misma arquitectura, menos red

---

## Plan B — Mensaje clave

> Aunque esté todo en un solo portátil,  
> **Spark sigue siendo distribuido**.

Los procesos son distintos  
y se comunican como si fueran máquinas diferentes.

---

## Plan B — Cuándo usarlo

✔ La red no permite conexiones entre alumnos  
✔ Firewalls o WiFi aislado  
✔ Equipos medianamente potentes  

👉 **Es el mejor plan B posible**

---

## 🅲 Plan C — Spark local (último recurso)

### ¿En qué consiste?
- Un solo proceso Spark
- Usa todos los núcleos del equipo
- Sin arquitectura visible de clúster

### Qué demuestra
- La API de Spark
- Paralelismo básico

---

## Plan C — Qué NO demuestra

❌ No se ve Master / Worker  
❌ No se ve clúster  
❌ Menos impacto conceptual  

👉 **Funciona, pero no es lo ideal**

---

## Plan C — Cuándo usarlo

✔ Equipo justo  
✔ Problemas con Docker  
✔ Necesidad de avanzar sí o sí  

👉 Es un **plan de emergencia**

---

## Comparación rápida

| Plan | Arquitectura | Red | Valor didáctico |
|----|-------------|-----|----------------|
| A | Clúster real | Sí | ⭐⭐⭐ |
| B | Clúster local | No | ⭐⭐⭐ |
| C | Local | No | ⭐ |

---

## Lo más importante

### 🔑 El código es el mismo

- Mismos scripts
- Mismas operaciones
- Mismos conceptos

Solo cambia **dónde se ejecuta**

---

## Mensaje final

> En Big Data real,  
> la infraestructura **nunca es perfecta**.

Lo importante es:
- entender el modelo
- saber adaptarse
- y que los datos se procesen

---

## Ahora sí…

👉 Empezamos el laboratorio de Spark