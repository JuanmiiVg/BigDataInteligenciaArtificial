# Sistema de Alerta de Tráfico - Lógica Difusa

## Descripción del Proyecto

Este proyecto implementa un **Sistema de Alerta de Tráfico** utilizando **Lógica Difusa** para determinar el nivel de congestión vehicular. El sistema evalúa dos variables principales: la cantidad de vehículos y la velocidad promedio de circulación, generando alertas clasificadas en tres niveles: baja, media y alta.

## Problema Resuelto

### Contexto del Problema
El control y monitoreo del tráfico vehicular es un desafío complejo en las ciudades modernas. Los sistemas tradicionales basados en reglas discretas (booleanas) no pueden manejar eficientemente la **incertidumbre** y **variabilidad** inherente al comportamiento del tráfico.

### Variables del Sistema

#### Variables de Entrada:
- **Vehículos**: Cantidad de vehículos por kilómetro (0-100)
  - **Pocos**: 0-30 vehículos/km
  - **Moderados**: 20-60 vehículos/km  
  - **Muchos**: 50-100 vehículos/km

- **Velocidad Promedio**: Velocidad en km/h (0-120)
  - **Lenta**: 0-40 km/h
  - **Media**: 30-80 km/h
  - **Rápida**: 70-120 km/h

#### Variable de Salida:
- **Alerta**: Nivel de congestión (0-10)
  - **Baja**: 0-4 (🟢 Tráfico fluido)
  - **Media**: 3-7 (🟡 Congestión moderada)
  - **Alta**: 6-10 (🔴 Congestión severa)

### Reglas de Inferencia

El sistema utiliza 9 reglas difusas basadas en conocimiento experto:

1. **Pocos vehículos + Velocidad rápida** → Alerta **BAJA**
2. **Pocos vehículos + Velocidad media** → Alerta **BAJA**
3. **Pocos vehículos + Velocidad lenta** → Alerta **MEDIA**
4. **Vehículos moderados + Velocidad rápida** → Alerta **BAJA**
5. **Vehículos moderados + Velocidad media** → Alerta **MEDIA**
6. **Vehículos moderados + Velocidad lenta** → Alerta **ALTA**
7. **Muchos vehículos + Velocidad rápida** → Alerta **MEDIA**
8. **Muchos vehículos + Velocidad media** → Alerta **ALTA**
9. **Muchos vehículos + Velocidad lenta** → Alerta **ALTA**

## Implementación Técnica

### Librerías Utilizadas
- **scikit-fuzzy**: Motor de lógica difusa
- **NumPy**: Operaciones numéricas
- **Matplotlib**: Visualización de datos

### Arquitectura del Sistema
```
Entradas → Fuzzificación → Motor de Inferencia → Defuzzificación → Salida
```

1. **Fuzzificación**: Conversión de valores numéricos a grados de pertenencia difusos
2. **Motor de Inferencia**: Aplicación de reglas difusas usando operadores MIN-MAX
3. **Defuzzificación**: Conversión del resultado difuso a valor numérico (centroide)

### Funciones de Pertenencia
- **Trapezoidales**: Para valores extremos (pocos/muchos vehículos, lenta/rápida velocidad)
- **Triangulares**: Para valores intermedios (moderados vehículos, velocidad media)

## Análisis Comparativo

### ¿Es posible resolver el problema usando reglas discretas?

**Respuesta: Técnicamente SÍ, pero NO es recomendable.**

#### Ventajas de Reglas Discretas:
- Simplicidad de implementación
- Ejecución rápida
- Fácil debugging

#### Desventajas Críticas de Reglas Discretas:
- **Pérdida de información**: Los umbrales fijos eliminan matices importantes
- **Comportamiento abrupto**: Cambios drásticos en la salida por pequeñas variaciones en la entrada
- **Falta de flexibilidad**: No se adapta a condiciones intermedias o ambiguas
- **Sobreajuste**: Requiere múltiples reglas específicas para cubrir todos los casos

#### Ejemplo Comparativo:
```
Escenario: 49 vehículos/km a 41 km/h vs 51 vehículos/km a 39 km/h

REGLAS DISCRETAS:
- Caso 1: IF vehiculos < 50 AND velocidad > 40 THEN alerta = BAJA
- Caso 2: IF vehiculos > 50 AND velocidad < 40 THEN alerta = ALTA
- Resultado: Salto abrupto de BAJA a ALTA por diferencias mínimas

LÓGICA DIFUSA:
- Ambos casos generan alertas similares (nivel medio-alto)
- Transición suave y proporcional a las diferencias reales
```

### ¿Por qué la Lógica Difusa es Superior?

1. **Manejo de Incertidumbre**: El tráfico es inherentemente impreciso y variable
2. **Transiciones Suaves**: Evita cambios abruptos en las decisiones
3. **Flexibilidad**: Fácil ajuste de parámetros sin reescribir reglas
4. **Robustez**: Tolerante a ruido en sensores y variaciones menores

## Integración en Flujo de Automatización

### ¿Puede integrarse en un flujo de automatización?

**Respuesta: SÍ, completamente.**

### Casos de Uso en Automatización:

#### 1. **Sistema de Semáforos Inteligentes**
```
Flujo de Automatización:
Sensores → Sistema Difuso → Controlador de Semáforos → Ajuste de Tiempos

Implementación:
- Sensores detectan vehículos y velocidad cada 30 segundos
- Sistema difuso calcula nivel de alerta
- Controlador ajusta duración de semáforos:
  * Alerta BAJA: Ciclos normales (60s verde)
  * Alerta MEDIA: Ciclos extendidos (90s verde)
  * Alerta ALTA: Ciclos de emergencia (120s verde + coordinación)
```

#### 2. **Gestión de Rutas Dinámicas**
```
Flujo de Automatización:
Sistema Difuso → API de Navegación → Apps de Usuarios

Proceso:
- Análisis continuo de múltiples vías
- Identificación de rutas con alerta alta
- Redirección automática de tráfico a rutas alternativas
- Notificaciones push a usuarios
```

#### 3. **Control de Acceso Vial**
```
Flujo de Automatización:
Sistema Difuso → Barreras/Señales → Control de Acceso

Acciones basadas en alerta:
- BAJA: Acceso libre
- MEDIA: Señalización preventiva
- ALTA: Restricción temporal de acceso
```

#### 4. **Integración IoT Inteligente**
```
Arquitectura del Sistema:
┌─────────────┐    ┌──────────────┐    ┌─────────────────┐
│  Sensores   │───▶│ Edge Gateway │───▶│ Sistema Difuso  │
│   IoT       │    │   (5G/WiFi)  │    │   (Cloud/Edge)  │
└─────────────┘    └──────────────┘    └─────────────────┘
                                                  │
┌─────────────┐    ┌──────────────┐    ┌─────────────────┐
│ Actuadores  │◀───│   Message    │◀───│ Decisiones      │
│ (Semáforos) │    │    Queue     │    │ Automatizadas   │
└─────────────┘    └──────────────┘    └─────────────────┘
```

### Ventajas en Automatización:

1. **Tiempo Real**: Respuesta inmediata a cambios en condiciones
2. **Escalabilidad**: Aplicable a redes viales completas
3. **Adaptabilidad**: Ajuste automático a patrones de tráfico
4. **Integración**: Compatible con múltiples sistemas (IoT, APIs, databases)

## Instalación y Uso

### Requisitos:
```bash
pip install scikit-fuzzy numpy matplotlib
```

### Ejecución:
```python
from sistema_alerta_trafico import SistemaAlertaTrafico

# Crear sistema
sistema = SistemaAlertaTrafico()

# Evaluar condiciones
nivel, categoria = sistema.calcular_alerta(vehiculos=45, velocidad_promedio=35)
print(f"Nivel de alerta: {nivel:.2f} - Categoría: {categoria}")
```

## Validación del Sistema

### Casos de Prueba Incluidos:
1. **Tráfico fluido**: 10 veh/km @ 80 km/h → Alerta BAJA
2. **Congestión moderada**: 25 veh/km @ 45 km/h → Alerta MEDIA  
3. **Congestión severa**: 60 veh/km @ 30 km/h → Alerta ALTA
4. **Embotellamiento**: 80 veh/km @ 15 km/h → Alerta ALTA
5. **Autopista rápida**: 35 veh/km @ 90 km/h → Alerta BAJA

## Conclusiones

### Criterios de Evaluación Cubiertos:

#### 2c) Modelos de Automatización
- **Pregunta**: ¿Se puede integrar en automatización? **SÍ**
- **Ejemplo**: Semáforos inteligentes, control IoT, gestión de rutas

#### 2d) Razonamiento Impreciso
- **Problema idóneo**: Tráfico vehicular con incertidumbre natural
- **Código limpio**: Implementación completa y documentada
- **Comentarios exhaustivos**: Cada función explicada detalladamente

#### 2e) Sistemas Basados en Reglas
- **Pregunta**: ¿Es posible con reglas discretas? **SÍ, pero inadecuado**
- **Justificación**: Pérdida de información, transiciones abruptas, falta de flexibilidad

### Impacto del Proyecto:
Este sistema demuestra cómo la lógica difusa proporciona una solución más natural y robusta para problemas del mundo real que involucran incertidumbre e imprecisión, siendo especialmente valioso en sistemas de automatización donde las decisiones graduales superan a las respuestas binarias.

---
**Autor**: Juan Manuel Vega  
**Fecha**: Febrero 2026  
**Curso**: Sistemas de Aprendizaje Automático