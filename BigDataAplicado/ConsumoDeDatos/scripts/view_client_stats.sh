#!/bin/bash
# Script para ver estadísticas de un cliente

if [ -z "$1" ]; then
    CLIENTE="CLI_00001"
else
    CLIENTE=$1
fi

echo "📊 Estadísticas del cliente: $CLIENTE"
echo ""

curl -s http://localhost:8001/api/estadisticas/cliente/$CLIENTE | jq .

echo ""
