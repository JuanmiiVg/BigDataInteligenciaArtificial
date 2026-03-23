# Guía de Inicio Rápido - Sistema de Alerta de Tráfico

## 🚀 Instalación

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Verificar instalación:**
```bash
python test_rapido.py
```

## 📋 Archivos del Proyecto

- `sistema_alerta_trafico.py` - **Código principal del sistema**
- `README.md` - Documentación completa del proyecto
- `ejemplos_demostracion.py` - Ejemplos y casos de uso
- `test_rapido.py` - Prueba de verificación del sistema
- `requirements.txt` - Dependencias necesarias
- `QUICK_START.md` - Esta guía de inicio rápido

## ⚡ Uso Básico

```python
from sistema_alerta_trafico import SistemaAlertaTrafico

# Crear sistema
sistema = SistemaAlertaTrafico()

# Evaluar situación de tráfico
nivel, categoria = sistema.calcular_alerta(
    num_vehiculos=45,      # vehículos por km
    velocidad_promedio=35  # km/h
)

print(f"Nivel de alerta: {nivel:.1f} - Categoría: {categoria}")
```

## 🎯 Ejemplos Rápidos

### Ejemplo 1: Tráfico Fluido
```python
nivel, categoria = sistema.calcular_alerta(15, 75)
# Resultado: Alerta BAJA (tráfico fluido)
```

### Ejemplo 2: Congestión
```python
nivel, categoria = sistema.calcular_alerta(70, 25)
# Resultado: Alerta ALTA (congestión severa)
```

## 📊 Visualizaciones

```python
# Funciones de pertenencia
sistema.visualizar_funciones_pertenencia()

# Superficie de control 3D
sistema.superficie_control()

import matplotlib.pyplot as plt
plt.show()
```

## 🎮 Modo Interactivo

```bash
python ejemplos_demostracion.py
```

## 📖 Documentación Completa

Consulte `README.md` para:
- Teoría de lógica difusa aplicada
- Comparación con reglas discretas  
- Integración en sistemas de automatización
- Análisis detallado del problema

## ⚙️ Configuración del Sistema

Las variables difusas están preconfiguradas con valores óptimos:

**Vehículos por km:**
- Pocos: 0-30
- Moderados: 20-60
- Muchos: 50-100

**Velocidad (km/h):**
- Lenta: 0-40
- Media: 30-80
- Rápida: 70-120

**Niveles de Alerta:**
- Baja: 0-4 🟢
- Media: 3-7 🟡  
- Alta: 6-10 🔴

## 🚨 Resolución de Problemas

**Error de importación:**
```bash
pip install scikit-fuzzy numpy matplotlib
```

**Error de ejecución:**
```bash
python test_rapido.py
```

## 📞 Soporte

Para preguntas sobre la implementación, consulte:
1. `README.md` - Documentación completa
2. `ejemplos_demostracion.py` - Casos de uso detallados
3. Comentarios en el código fuente

---
**Developed by:** Juan Manuel Vega  
**Course:** Sistemas de Aprendizaje Automático  
**Date:** Febrero 2026