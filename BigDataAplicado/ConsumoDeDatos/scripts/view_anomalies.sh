#!/bin/bash
# Script para ver top anomalías

echo "🚨 Top anomalías detectadas..."
echo ""

curl -s http://localhost:8001/api/dashboard/top-anomalias?limit=15 | jq .

echo ""
