#!/bin/bash

echo "🚀 Iniciando Sistema de Monitoreo de Consumo..."
echo "================================================"

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker no está instalado${NC}"
    exit 1
fi

echo -e "${BLUE}✓ Docker detectado${NC}"

# Compilar y ejecutar
echo -e "${YELLOW}📦 Compilando y ejecutando servicios...${NC}"
docker-compose up --build

echo -e "${GREEN}✓ Sistema iniciado${NC}"
echo ""
echo -e "${BLUE}Accede a los servicios:${NC}"
echo "  🌐 Frontend:      http://localhost:8501"
echo "  📊 Backend API:   http://localhost:8001"
echo "  🔌 Data Gen API:  http://localhost:8000"
echo "  📡 Kafka:         localhost:9092"
echo "  🗄️  MongoDB:      localhost:27017"
echo ""
echo -e "${YELLOW}Para ver logs:${NC}"
echo "  docker-compose logs -f"
echo ""
echo -e "${YELLOW}Para detener:${NC}"
echo "  docker-compose down"
