## Ejemplo de importación de datasets
Para importar datasets en una colección de MondoDB Atlas vamos a optar por la utilidad de comandos mongoimport.

Como dataset vamos a usar los datos de población mundial en 2025. 

### Mongoimport:
[Documentación de instalación](https://www.mongodb.com/docs/database-tools/mongoimport/)

### Datos de ejemplo:
[Población mundial 2025](https://www.kaggle.com/datasets/asadullahcreative/world-population-by-country-2025?resource=download)

[population_data.csv](population_data.csv)

### Comando de importación:
```
mongoimport --uri=mongodb+srv://cluster0.4kofg1a.mongodb.net/ -d big-data-aplicado -c datos-prueba -u admin --headerline --type=csv population_data.csv
```

