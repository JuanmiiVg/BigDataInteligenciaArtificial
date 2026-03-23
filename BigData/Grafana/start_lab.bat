@echo off
echo ================================================
echo    LABORATORIO GRAFANA - INICIANDO SERVICIOS
echo ================================================
echo.

echo [INFO] Verificando Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker no esta disponible. Asegurate de que Docker Desktop este ejecutandose.
    pause
    exit /b 1
)
echo [OK] Docker disponible

echo.
echo [INFO] Iniciando contenedores de Grafana + Prometheus + Simulador...
docker-compose up -d

echo.
echo [INFO] Esperando a que los servicios esten listos...
timeout /t 15 /nobreak >nul

echo.
echo ================================================
echo           SERVICIOS INICIADOS
echo ================================================
echo.
echo 📊 GRAFANA:     http://localhost:3000
echo    Usuario:    admin
echo    Password:   admin123
echo.
echo 📈 PROMETHEUS:  http://localhost:9090
echo.
echo 🔧 METRICAS:    http://localhost:8000/metrics
echo.
echo ================================================
echo           PASOS SIGUIENTES:
echo ================================================
echo 1. Abre Grafana en tu navegador: http://localhost:3000
echo 2. Inicia sesion con admin/admin123
echo 3. Configura Prometheus como Data Source: http://prometheus:9090
echo 4. Crea los paneles del laboratorio
echo.
echo Para detener: docker-compose down
echo ================================================

pause