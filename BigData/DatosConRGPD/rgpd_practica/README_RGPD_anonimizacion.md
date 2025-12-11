# Actividad RGPD: Anonimización y uso del dataset en calidad e integración

Contenido:

- `clientes_raw.csv`: dataset con datos personales (~300 clientes).
- `ventas_clientes.csv`: ~1000 ventas asociadas a esos clientes.

Sugerencia de uso:

1. Anonimizar `clientes_raw.csv`:
   - crear `id_hash` con hash de `id_cliente`,
   - eliminar nombre, apellidos, email, teléfono,
   - generalizar código postal (3 dígitos) y/o fecha de nacimiento (décadas).

2. Integrar con `ventas_clientes.csv`:
   - reemplazar `id_cliente` por `id_hash` en la tabla de ventas,
   - obtener `ventas_clientes_anon.csv`.

3. Reutilizar `ventas_clientes_anon.csv` en prácticas de:
   - calidad de datos (reglas de dominio, rango, consistencia),
   - integración con otras fuentes.
