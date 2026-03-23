# =========================================================
# setup-debezium.ps1
# Registro del conector Debezium PostgreSQL CDC
# =========================================================

$connector = @{
    name = "postgres-cdc-connector"
    config = @{
        "connector.class" = "io.debezium.connector.postgresql.PostgresConnector"
        "database.hostname" = "postgres"
        "database.port" = "5432"
        "database.user" = "postgres"
        "database.password" = "postgres"
        "database.dbname" = "empresa"
        "topic.prefix" = "cdc"
        "table.include.list" = "public.clientes,public.productos,public.pedidos"
        "plugin.name" = "pgoutput"
    }
}

$body = $connector | ConvertTo-Json -Depth 5

Invoke-RestMethod `
    -Method Post `
    -Uri "http://localhost:8083/connectors" `
    -ContentType "application/json" `
    -Body $body

Write-Host "✅ Conector Debezium creado correctamente"
