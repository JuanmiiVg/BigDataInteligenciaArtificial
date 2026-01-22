# 📋 Estructura de Documentación

## Archivos Markdown

```
ConsumoDeDatos/
├── START_HERE.md          ← Punto de entrada rápido (60 segundos)
├── README.md              ← Guía principal y características
├── QUICK_START.md         ← Instalación y primeros pasos
└── DOCS.md                ← Documentación técnica completa

Otros archivos importantes:
├── docker-compose.yml     ← Orquestación de servicios
├── requirements.txt       ← Dependencias Python
├── Dockerfile.*           ← Imágenes Docker
└── ...
```

## Flujo Recomendado de Lectura

### 👤 Nuevo Usuario
1. **[START_HERE.md](START_HERE.md)** - 2 min - Qué es, cómo empezar
2. **[README.md](README.md)** - 5 min - Características principales
3. **[QUICK_START.md](QUICK_START.md)** - 10 min - Instalación paso a paso
4. **[DOCS.md](DOCS.md)** - Referencia - Consulta según necesites

### 👨‍💻 Desarrollador
1. **[README.md](README.md)** - Visión general
2. **[DOCS.md](DOCS.md)** → Secciones relevantes:
   - Arquitectura
   - Componentes Core
   - Base de Datos
   - API REST
   - Comandos Útiles

### 🔧 DevOps/Infraestructura
1. **[DOCS.md](DOCS.md)** → Secciones:
   - Stack Tecnológico
   - Configuración
   - Comandos Útiles
   - Troubleshooting

### 🐛 Debugging
1. **[DOCS.md](DOCS.md)** → Sección: Troubleshooting

---

## Consolidación Realizada

**Antes**: 28 archivos Markdown
- 24 archivos archivados/redundantes
- Difícil de mantener para Git

**Ahora**: 4 archivos Markdown
- Todo organizado y actualizado
- Fácil de mantener en repositorio
- Referenciación cruzada clara

### Archivos Eliminados

✂️ Reportes de proyecto:
- ENTREGA_FINAL.md
- ESTADO_FINAL_V2.0.md
- RESUMEN_ENTREGA.md
- RESUMEN_V2.0.md
- COMPLETED.md

✂️ Documentación duplicada/archivada:
- BIGDATA_ARCHITECTURE.md (→ DOCS.md)
- BIGDATA_SETUP.md (→ DOCS.md)
- TECHNICAL_DOCS.md (→ DOCS.md)
- COMANDOS_RAPIDOS.md (→ DOCS.md)
- DOCUMENTACION_COMPLETA.md (→ DOCS.md)
- ARCHIVADO_DATOS.md
- QUICK_REFERENCE_ARCHIVADO.md
- Otros indices, mapas y guides redundantes

---

## URLs Rápidas

```
🌐 Frontend:            http://localhost:8501
🔌 API REST:            http://localhost:8001
📚 API Docs Swagger:     http://localhost:8001/docs
```

---

**Para empezar: Lee [START_HERE.md](START_HERE.md)**
