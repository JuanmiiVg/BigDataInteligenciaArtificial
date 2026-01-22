#!/bin/bash
# Script para monitorear logs en tiempo real

echo "📋 Logs en tiempo real"
echo "====================="
echo ""
echo "Presiona Ctrl+C para detener"
echo ""

docker-compose logs -f --tail=100
