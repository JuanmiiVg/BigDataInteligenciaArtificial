#!/bin/bash
# Script para generar datos de prueba

echo "📊 Generando datos de prueba..."
echo ""

# Generar batch una sola vez
echo "Generando batch de 20 clientes (5 sospechosos)..."
curl -X POST "http://localhost:8000/generar/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "num_clientes": 20,
    "num_sospechosos": 5
  }' | jq .

echo ""
echo "✓ Datos generados"
