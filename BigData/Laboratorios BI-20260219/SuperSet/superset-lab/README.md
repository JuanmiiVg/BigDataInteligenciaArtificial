# Superset Lab (UD4)

## Requisitos
- Docker Desktop encendido

## Arranque
1. Abrir terminal en esta carpeta
2. Ejecutar:

```powershell
docker compose up -d
```

3. Comprobar estado:

```powershell
docker ps
```

4. Acceder a Superset:
- URL: http://localhost:8088
- Usuario: admin
- Password: admin

## Parar

```powershell
docker compose down
```

## Limpiar completamente (opcional)

```powershell
docker compose down -v
```

## Siguiente paso del laboratorio
- En Superset: Settings > Database Connections > + Database
- Añadir conexión a la misma base que usaste en Metabase
- Realizar captura con estado "Successful"
