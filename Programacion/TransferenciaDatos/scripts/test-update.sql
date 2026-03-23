-- =========================================================
-- test-update.sql
-- Prueba CDC: UPDATE
-- =========================================================

UPDATE clientes
SET nombre = 'ALUMNO MODIFICADO'
WHERE email = 'alumno@test.com';