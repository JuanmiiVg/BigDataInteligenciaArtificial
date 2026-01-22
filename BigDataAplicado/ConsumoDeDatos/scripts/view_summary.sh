#!/bin/bash
# Script para ver resumen global

echo "📈 Resumen global de anomalías (últimas 24h)"
echo ""

curl -s http://localhost:8001/api/estadisticas/resumen | jq .

echo ""
