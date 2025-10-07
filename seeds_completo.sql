-- seeds_completo.sql
USE mantenimiento;

-- ----------------------------
-- REINICIO DE TABLAS
-- ----------------------------
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS tareas, equipos, estados_equipo, agencias, unidades_negocio, ciudades, provincias, proyectos, clientes, roles;
DROP TABLE IF EXISTS usuarios, refresh_tokens, parametros, actividades, posibles_respuestas; -- Limpia también las tablas existentes
SET FOREIGN_KEY_CHECKS=1;

-- ----------------------------
-- CREACIÓN DE ESTRUCTURA
-- ----------------------------
CREATE TABLE roles (id INT PRIMARY KEY, nombre VARCHAR(100) NOT NULL UNIQUE);
CREATE TABLE usuarios (id INT PRIMARY KEY AUTO_INCREMENT, nombre VARCHAR(120) NOT NULL, email VARCHAR(160) NOT NULL UNIQUE, password_hash VARCHAR(255) NOT NULL, rol_id INT NOT NULL, activo BOOLEAN NOT NULL DEFAULT TRUE, FOREIGN KEY (rol_id) REFERENCES roles(id));
CREATE TABLE clientes (id INT PRIMARY KEY, nombre VARCHAR(100) NOT NULL UNIQUE, nombre_completo VARCHAR(255));
CREATE TABLE proyectos (id INT PRIMARY KEY, nombre TEXT NOT NULL, cliente_id INT NOT NULL, FOREIGN KEY (cliente_id) REFERENCES clientes(id));
CREATE TABLE provincias (id INT PRIMARY KEY, nombre VARCHAR(100) NOT NULL UNIQUE);
CREATE TABLE ciudades (id INT PRIMARY KEY, nombre VARCHAR(100) NOT NULL, provincia_id INT NOT NULL, FOREIGN KEY (provincia_id) REFERENCES provincias(id));
CREATE TABLE unidades_negocio (id INT PRIMARY KEY, nombre VARCHAR(255) NOT NULL);
CREATE TABLE agencias (id INT PRIMARY KEY, nombre VARCHAR(255) NOT NULL, ciudad_id INT NOT NULL, unidad_negocio_id INT NOT NULL, FOREIGN KEY (ciudad_id) REFERENCES ciudades(id), FOREIGN KEY (unidad_negocio_id) REFERENCES unidades_negocio(id));
CREATE TABLE estados_equipo (id INT PRIMARY KEY, nombre VARCHAR(50) NOT NULL UNIQUE);
CREATE TABLE equipos (id VARCHAR(50) PRIMARY KEY, nombre VARCHAR(100) NOT NULL, modelo VARCHAR(100) NOT NULL, caracteristicas TEXT, cliente_id INT, proyecto_id INT, provincia_id INT, ciudad_id INT, unidad_negocio_id INT, agencia_id INT, estado_id INT, FOREIGN KEY (cliente_id) REFERENCES clientes(id), FOREIGN KEY (proyecto_id) REFERENCES proyectos(id), FOREIGN KEY (provincia_id) REFERENCES provincias(id), FOREIGN KEY (ciudad_id) REFERENCES ciudades(id), FOREIGN KEY (unidad_negocio_id) REFERENCES unidades_negocio(id), FOREIGN KEY (agencia_id) REFERENCES agencias(id), FOREIGN KEY (estado_id) REFERENCES estados_equipo(id));
CREATE TABLE tareas (id INT PRIMARY KEY AUTO_INCREMENT, usuario_id INT NOT NULL, equipo_id VARCHAR(50) NOT NULL, FOREIGN KEY (usuario_id) REFERENCES usuarios(id), FOREIGN KEY (equipo_id) REFERENCES equipos(id));
-- Aquí puedes añadir las otras tablas como 'parametros', 'actividades', etc.

-- ----------------------------
-- INSERCIÓN DE DATOS
-- ----------------------------
-- Catálogos
INSERT INTO roles (id, nombre) VALUES (1, 'Técnico de Campo'), (2, 'Supervisor');
INSERT INTO clientes (id, nombre, nombre_completo) VALUES (1, 'cnel', 'CORPORACION NACIONAL DE ELECTRICIDAD CNEL EP');
INSERT INTO proyectos (id, nombre, cliente_id) VALUES (1, 'CORP SERVICIO DE SOPORTE MANTENIMIENTO Y GARANTÍA DE LOS EQUIPOS DE NETWORKING HUAWEI DE CNEL EP GTI', 1);
INSERT INTO provincias (id, nombre) VALUES (9, 'GUAYAS'), (13, 'MANABI');
INSERT INTO ciudades (id, nombre, provincia_id) VALUES (1, 'MANTA', 13), (2, 'PORTOVIEJO', 13), (3, 'GUAYAQUIL', 9), (4, 'DURAN', 9);
INSERT INTO unidades_negocio (id, nombre) VALUES (1, 'GUAYAS'), (2, 'GUAYAS - LOS RIOS'), (3, 'MANABI');
INSERT INTO agencias (id, nombre, ciudad_id, unidad_negocio_id) VALUES (1, 'AGENCIA GUAYAQUIL', 3, 1), (2, 'AGENCIA GUAYACANES', 3, 1), (3, 'AGENCIA DURAN', 4, 2), (4, 'AGENCIA RECREO', 4, 2), (5, 'SUBESTACION MANTA 1', 1, 3), (6, 'EQUIPOS EN POSTE', 1, 3), (7, 'AGENCIA PRIZA', 2, 3), (8, 'AGENCIA PORTOVIEJO COMERCIAL', 2, 3);
INSERT INTO estados_equipo (id, nombre) VALUES (1, 'pendiente'), (2, 'en progreso'), (3, 'completado');

-- Usuarios (Contraseñas hasheadas: '123' y '456')
INSERT INTO usuarios (id, nombre, email, password_hash, rol_id, activo) VALUES
(101, 'Juan Perez', 'jp@email.com', '$2b$12$Gz6A6OAcon42b8d00e.D9uW2z2wm8rev79/UC3S9a9g2mD5.O.mIq', 1, TRUE),
(102, 'Maria Lopez', 'ml@email.com', '$2b$12$Y/i1Y0fMv/f9y3oZg.kSTeUa8d298Wb.gmPjD/c9xXzR.Rk4/Jc0K', 1, TRUE);

-- Equipos
INSERT INTO equipos (id, nombre, modelo, caracteristicas, cliente_id, proyecto_id, provincia_id, ciudad_id, unidad_negocio_id, agencia_id, estado_id) VALUES
('21980107133GJ7000257', 'SWITCH CAPA 3', 'S5730-68C-SI-AC', '(48 Ethernet 10/100/1000 ports,4 10 Gig SFP+, AC 110/220V)', 1, 1, 9, 3, 1, 1, 1),
('21980105812SJ4600371', 'SWITCH CAPA 2', 'S5720-28X-LI-AC', '(24 Ethernet 10/100/1000 ports, 4 10 Gig SFP+, AC 110/220V)', 1, 1, 9, 3, 1, 1, 1),
('21980105812SJ4600293', 'SWITCH CAPA 2', 'S5720-28X-LI-AC', '(24 Ethernet 10/100/1000 ports, 4 10 Gig SFP+, AC 110/220V)', 1, 1, 9, 3, 1, 2, 1),
('21980105812SJ4600373', 'SWITCH CAPA 2', 'S5720-28X-LI-AC', '(24 Ethernet 10/100/1000 ports, 4 10 Gig SFP+, AC 110/220V)', 1, 1, 9, 3, 1, 2, 1),
('21980105812SJ4600325', 'SWITCH CAPA 2', 'S5720-28X-LI-AC', '(24 Ethernet 10/100/1000 ports, 4 10 Gig SFP+, AC 110/220V)', 1, 1, 9, 4, 2, 3, 1),
('21980105812SJ4600297', 'SWITCH CAPA 2', 'S5720-28X-LI-AC', '(24 Ethernet 10/100/1000 ports, 4 10 Gig SFP+, AC 110/220V)', 1, 1, 9, 4, 2, 4, 1),
('21980105812SJ4600326', 'SWITCH CAPA 2', 'S5720-28X-LI-AC', '(24 Ethernet 10/100/1000 ports, 4 10 Gig SFP+, AC 110/220V)', 1, 1, 13, 1, 3, 5, 1),
('21980105812SJ4600318', 'SWITCH CAPA 2', 'S5720-28X-LI-AC', '(24 Ethernet 10/100/1000 ports, 4 10 Gig SFP+, AC 110/220V)', 1, 1, 13, 1, 3, 5, 1),
('21980105812SJ4600315', 'SWITCH CAPA 2', 'S5720-28X-LI-AC', '(24 Ethernet 10/100/1000 ports, 4 10 Gig SFP+, AC 110/220V)', 1, 1, 13, 1, 3, 6, 1),
('21980107133GJ7000255', 'SWITCH CAPA 3', 'S5730-68C-SI-AC', '(48 Ethernet 10/100/1000 ports,4 10 Gig SFP+, AC 110/220V)', 1, 1, 13, 2, 3, 7, 1),
('21980105812SJ4600336', 'SWITCH CAPA 2', 'S5720-28X-LI-AC', '(24 Ethernet 10/100/1000 ports, 4 10 Gig SFP+, AC 110/220V)', 1, 1, 13, 2, 3, 7, 1),
('21980105812SJ4600332', 'SWITCH CAPA 2', 'S5720-28X-LI-AC', '(24 Ethernet 10/100/1000 ports, 4 10 Gig SFP+, AC 110/220V)', 1, 1, 13, 2, 3, 8, 1),
('21980105812SJ4600322', 'SWITCH CAPA 2', 'S5720-28X-LI-AC', '(24 Ethernet 10/100/1000 ports, 4 10 Gig SFP+, AC 110/220V)', 1, 1, 13, 2, 3, 8, 1),
('21980105812SJ4600338', 'SWITCH CAPA 2', 'S5720-28X-LI-AC', '(24 Ethernet 10/100/1000 ports, 4 10 Gig SFP+, AC 110/220V)', 1, 1, 13, 2, 3, 8, 1),
('21980105812SJ4600317', 'SWITCH CAPA 2', 'S5720-28X-LI-AC', '(24 Ethernet 10/100/1000 ports, 4 10 Gig SFP+, AC 110/220V)', 1, 1, 13, 2, 3, 8, 1);

-- Tareas
INSERT INTO tareas (id, usuario_id, equipo_id) VALUES
(1, 101, '21980107133GJ7000257'), (2, 101, '21980105812SJ4600371'), (3, 101, '21980105812SJ4600293'),
(4, 101, '21980105812SJ4600373'), (5, 101, '21980105812SJ4600325'), (6, 101, '21980105812SJ4600326'),
(7, 101, '21980105812SJ4600318'), (8, 102, '21980105812SJ4600297'), (9, 102, '21980105812SJ4600315'),
(10, 102, '21980107133GJ7000255'), (11, 102, '21980105812SJ4600336'), (12, 102, '21980105812SJ4600332'),
(13, 102, '21980105812SJ4600322'), (14, 102, '21980105812SJ4600338'), (15, 102, '21980105812SJ4600317');