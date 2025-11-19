-- seeds_definitivo_v2.sql
-- Script único y completo para crear y poblar toda la base de datos.
-- ----------------------------------------------------------------

USE mantenimiento;

-- ----------------------------
-- REINICIO COMPLETO DE TABLAS
-- ----------------------------
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS
    tareas,
    equipos,
    estados_equipo,
    posibles_respuestas,
    actividades,
    agencias,
    unidades_negocio,
    ciudades,
    provincias,
    proyectos,
    clientes,
    refresh_tokens,
    parametros,
    usuarios,
    roles;
SET FOREIGN_KEY_CHECKS=1;

-- ----------------------------
-- CREACIÓN DE ESTRUCTURA COMPLETA
-- ----------------------------
CREATE TABLE roles (id INT PRIMARY KEY, nombre VARCHAR(100) NOT NULL UNIQUE);
CREATE TABLE usuarios (id INT PRIMARY KEY, nombre VARCHAR(120) NOT NULL, email VARCHAR(160) NOT NULL UNIQUE, password_hash VARCHAR(255) NOT NULL, rol_id INT NOT NULL, activo BOOLEAN NOT NULL DEFAULT TRUE, FOREIGN KEY (rol_id) REFERENCES roles(id));
CREATE TABLE refresh_tokens (id INT PRIMARY KEY AUTO_INCREMENT, user_id INT NOT NULL, token_hash CHAR(64) NOT NULL UNIQUE, issued_at DATETIME NOT NULL, expires_at DATETIME NOT NULL, revoked BOOLEAN NOT NULL DEFAULT FALSE, user_agent VARCHAR(255), ip VARCHAR(64), INDEX (user_id), INDEX (expires_at), FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE);
CREATE TABLE parametros (id INT PRIMARY KEY AUTO_INCREMENT, clave VARCHAR(100) NOT NULL UNIQUE, valor VARCHAR(255) NOT NULL, tipo ENUM('int','string','bool','json') NOT NULL DEFAULT 'string', descripcion VARCHAR(255));
CREATE TABLE clientes (id INT PRIMARY KEY, nombre VARCHAR(100) NOT NULL UNIQUE, nombre_completo VARCHAR(255));
CREATE TABLE proyectos (id INT PRIMARY KEY, nombre TEXT NOT NULL, cliente_id INT NOT NULL, FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE);
CREATE TABLE provincias (id INT PRIMARY KEY, nombre VARCHAR(100) NOT NULL UNIQUE);
CREATE TABLE ciudades (id INT PRIMARY KEY, nombre VARCHAR(100) NOT NULL, provincia_id INT NOT NULL, FOREIGN KEY (provincia_id) REFERENCES provincias(id) ON DELETE CASCADE);
CREATE TABLE unidades_negocio (id INT PRIMARY KEY, nombre VARCHAR(255) NOT NULL);
CREATE TABLE agencias (id INT PRIMARY KEY, nombre VARCHAR(255) NOT NULL, ciudad_id INT NOT NULL, unidad_negocio_id INT NOT NULL, FOREIGN KEY (ciudad_id) REFERENCES ciudades(id) ON DELETE CASCADE, FOREIGN KEY (unidad_negocio_id) REFERENCES unidades_negocio(id) ON DELETE CASCADE);
CREATE TABLE estados_equipo (id INT PRIMARY KEY, nombre VARCHAR(50) NOT NULL UNIQUE);
CREATE TABLE equipos (id VARCHAR(50) PRIMARY KEY, nombre VARCHAR(100) NOT NULL, modelo VARCHAR(100) NOT NULL, caracteristicas TEXT, cliente_id INT, proyecto_id INT, provincia_id INT, ciudad_id INT, unidad_negocio_id INT, agencia_id INT, estado_id INT, FOREIGN KEY (cliente_id) REFERENCES clientes(id), FOREIGN KEY (proyecto_id) REFERENCES proyectos(id), FOREIGN KEY (provincia_id) REFERENCES provincias(id), FOREIGN KEY (ciudad_id) REFERENCES ciudades(id), FOREIGN KEY (unidad_negocio_id) REFERENCES unidades_negocio(id), FOREIGN KEY (agencia_id) REFERENCES agencias(id), FOREIGN KEY (estado_id) REFERENCES estados_equipo(id));
CREATE TABLE tareas (id INT PRIMARY KEY AUTO_INCREMENT, usuario_id INT NOT NULL, equipo_id VARCHAR(50) NOT NULL, FOREIGN KEY (usuario_id) REFERENCES usuarios(id), FOREIGN KEY (equipo_id) REFERENCES equipos(id) ON DELETE CASCADE);
CREATE TABLE actividades (id INT PRIMARY KEY, nombre TEXT NOT NULL, tipo ENUM('preventivo', 'correctivo', 'diagnostico') NOT NULL, tipo_respuesta ENUM('single_choice', 'multiple_choice') NOT NULL);
CREATE TABLE posibles_respuestas (id INT PRIMARY KEY AUTO_INCREMENT, actividad_id INT NOT NULL, label VARCHAR(255) NOT NULL, value VARCHAR(100) NOT NULL, respuesta_condicional ENUM('yes', 'no') NOT NULL, FOREIGN KEY (actividad_id) REFERENCES actividades(id) ON DELETE CASCADE);

-- ----------------------------
-- INSERCIÓN DE DATOS
-- ----------------------------
INSERT INTO roles (id, nombre) VALUES (1, 'Técnico de Campo'), (2, 'Supervisor');
INSERT INTO parametros (clave, valor, tipo, descripcion) VALUES ('sesion.ttl_minutos', '1440', 'int', 'Duración de la sesión en minutos (min 24h)');
INSERT INTO clientes (id, nombre, nombre_completo) VALUES (1, 'cnel', 'CORPORACION NACIONAL DE ELECTRICIDAD CNEL EP');
INSERT INTO proyectos (id, nombre, cliente_id) VALUES (1, 'CORP SERVICIO DE SOPORTE MANTENIMIENTO Y GARANTÍA DE LOS EQUIPOS DE NETWORKING HUAWEI DE CNEL EP GTI', 1);
INSERT INTO provincias (id, nombre) VALUES (9, 'GUAYAS'), (13, 'MANABI');
INSERT INTO ciudades (id, nombre, provincia_id) VALUES (1, 'MANTA', 13), (2, 'PORTOVIEJO', 13), (3, 'GUAYAQUIL', 9), (4, 'DURAN', 9);
INSERT INTO unidades_negocio (id, nombre) VALUES (1, 'GUAYAS'), (2, 'GUAYAS - LOS RIOS'), (3, 'MANABI');
INSERT INTO agencias (id, nombre, ciudad_id, unidad_negocio_id) VALUES (1, 'AGENCIA GUAYAQUIL', 3, 1), (2, 'AGENCIA GUAYACANES', 3, 1), (3, 'AGENCIA DURAN', 4, 2), (4, 'AGENCIA RECREO', 4, 2), (5, 'SUBESTACION MANTA 1', 1, 3), (6, 'EQUIPOS EN POSTE', 1, 3), (7, 'AGENCIA PRIZA', 2, 3), (8, 'AGENCIA PORTOVIEJO COMERCIAL', 2, 3);
INSERT INTO estados_equipo (id, nombre) VALUES (1, 'pendiente'), (2, 'en progreso'), (3, 'completado');

INSERT INTO usuarios (id, nombre, email, password_hash, rol_id, activo) VALUES
(101, 'Juan Perez', 'jp@email.com', '$5$rounds=535000$wG13L87Y5j8V.x.f$Q69R3b.r.x/6z8K/t1k.L.F.pG1sP5v2u.K', 1, TRUE),
(102, 'Maria Lopez', 'ml@email.com', '$5$rounds=535000$O5s.h.pL1k2p.7.L$J.s.x2t1k.u.4pL.8f.sE6aP1k2p.7.Ld8', 1, TRUE);