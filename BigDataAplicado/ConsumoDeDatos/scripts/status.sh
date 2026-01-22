#!/bin/bash
# Script para listar todos los servicios y su estado

echo "🐳 Estado de servicios Docker"
echo "============================="
echo ""

docker-compose ps

echo ""
echo "📊 Información de contenedores:"
echo ""

docker-compose exec -T mongodb mongosh --eval "db.adminCommand('ping')" 2>/dev/null && echo "✓ MongoDB: OK" || echo "✗ MongoDB: ERROR"
curl -s http://localhost:8000/health > /dev/null && echo "✓ Data Generator: OK" || echo "✗ Data Generator: ERROR"
curl -s http://localhost:8001/health > /dev/null && echo "✓ Backend API: OK" || echo "✗ Backend API: ERROR"

echo ""
