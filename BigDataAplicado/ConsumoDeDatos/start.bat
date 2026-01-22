@echo off
REM Script de inicio para Windows

echo.
echo ========================================
echo  Sistema de Monitoreo de Consumo
echo ========================================
echo.

REM Verificar Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker no esta instalado
    exit /b 1
)

echo [OK] Docker detectado
echo.
echo Compilando e iniciando servicios...
echo.

docker-compose up --build

echo.
echo [INFO] Sistema iniciado correctamente
echo.
echo Accede a los servicios:
echo   - Frontend:      http://localhost:8501
echo   - Backend API:   http://localhost:8001
echo   - Data Gen API:  http://localhost:8000
echo.
echo Para ver logs en otra terminal:
echo   docker-compose logs -f
echo.
echo Para detener:
echo   docker-compose down
echo.
