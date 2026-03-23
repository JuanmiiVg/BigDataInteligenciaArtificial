@echo off
echo ================================================
echo    LABORATORIO GRAFANA - DETENIENDO SERVICIOS
echo ================================================
echo.

echo [INFO] Deteniendo contenedores...
docker-compose down

echo.
echo [INFO] Limpiando recursos...
docker-compose down --volumes --remove-orphans

echo.
echo [OK] Servicios detenidos correctamente
echo.
pause