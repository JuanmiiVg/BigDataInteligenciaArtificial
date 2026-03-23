-- =========================================================
-- 01-init.sql
-- Inicialización de la base de datos empresa
-- Compatible con Debezium (CDC) y Airbyte
-- =========================================================

-- Tabla CLIENTES
CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    ciudad VARCHAR(100),
    actualizado TIMESTAMP DEFAULT NOW()
);

-- Tabla PRODUCTOS
CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    precio NUMERIC(10,2) NOT NULL,
    actualizado TIMESTAMP DEFAULT NOW()
);

-- Tabla PEDIDOS
CREATE TABLE IF NOT EXISTS pedidos (
    id SERIAL PRIMARY KEY,
    cliente_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    actualizado TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_cliente
        FOREIGN KEY(cliente_id)
        REFERENCES clientes(id),
    CONSTRAINT fk_producto
        FOREIGN KEY(producto_id)
        REFERENCES productos(id)
);

-- Datos iniciales CLIENTES
INSERT INTO clientes (nombre, email, ciudad)
VALUES
('Ana López', 'ana@empresa.com', 'Murcia'),
('Luis García', 'luis@empresa.com', 'Alicante');

-- Datos iniciales PRODUCTOS
INSERT INTO productos (nombre, precio)
VALUES
('Portátil', 899.99),
('Ratón inalámbrico', 25.50);

-- Datos iniciales PEDIDOS
INSERT INTO pedidos (cliente_id, producto_id, cantidad)
VALUES
(1, 1, 1),
(2, 2, 2);

-- Fin del script
