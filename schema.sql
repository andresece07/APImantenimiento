-- Crear base de datos (si no existe)
CREATE DATABASE IF NOT EXISTS mantenimiento CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE mantenimiento;

-- Roles
CREATE TABLE IF NOT EXISTS roles (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL UNIQUE
);

-- Usuarios
CREATE TABLE IF NOT EXISTS usuarios (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(120) NOT NULL,
  email VARCHAR(160) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  rol_id INT NOT NULL,
  activo BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (rol_id) REFERENCES roles(id)
);

-- Parametros
CREATE TABLE IF NOT EXISTS parametros (
  id INT PRIMARY KEY AUTO_INCREMENT,
  clave VARCHAR(100) NOT NULL UNIQUE,
  valor VARCHAR(255) NOT NULL,
  tipo ENUM('int','string','bool','json') NOT NULL DEFAULT 'string',
  descripcion VARCHAR(255) NULL,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

DELIMITER $$
CREATE TRIGGER IF NOT EXISTS parametros_chk_ttl_ins
BEFORE INSERT ON parametros
FOR EACH ROW
BEGIN
  IF NEW.clave='sesion.ttl_minutos' AND CAST(NEW.valor AS UNSIGNED) < 1440 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='El TTL mínimo de sesión es 1440 minutos (24h)';
  END IF;
END$$

CREATE TRIGGER IF NOT EXISTS parametros_chk_ttl_upd
BEFORE UPDATE ON parametros
FOR EACH ROW
BEGIN
  IF NEW.clave='sesion.ttl_minutos' AND CAST(NEW.valor AS UNSIGNED) < 1440 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='El TTL mínimo de sesión es 1440 minutos (24h)';
  END IF;
END$$
DELIMITER ;

-- Refresh tokens (sesiones)
CREATE TABLE IF NOT EXISTS refresh_tokens (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  token_hash CHAR(64) NOT NULL,
  issued_at DATETIME NOT NULL,
  expires_at DATETIME NOT NULL,
  revoked BOOLEAN NOT NULL DEFAULT FALSE,
  user_agent VARCHAR(255) NULL,
  ip VARCHAR(64) NULL,
  CONSTRAINT fk_refresh_user FOREIGN KEY (user_id) REFERENCES usuarios(id),
  UNIQUE (token_hash),
  INDEX idx_refresh_user (user_id),
  INDEX idx_refresh_expires (expires_at),
  INDEX idx_refresh_revoked (revoked)
);

-- Tareas (ejemplo)
CREATE TABLE IF NOT EXISTS tareas (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  titulo VARCHAR(200) NOT NULL,
  descripcion TEXT NULL,
  estado ENUM('pendiente','en_progreso','completada','cancelada') NOT NULL DEFAULT 'pendiente',
  usuario_id INT NULL, -- asignada a técnico
  creada_por INT NOT NULL,
  fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  fecha_actualizacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
  FOREIGN KEY (creada_por) REFERENCES usuarios(id)
);

-- Actividades de Mantenimiento
CREATE TABLE IF NOT EXISTS actividades (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nombre TEXT NOT NULL,
  tipo ENUM('preventivo', 'correctivo', 'diagnostico') NOT NULL,
  tipo_respuesta ENUM('single_choice', 'multiple_choice') NOT NULL
);

CREATE TABLE IF NOT EXISTS posibles_respuestas (
  id INT PRIMARY KEY AUTO_INCREMENT,
  actividad_id INT NOT NULL,
  label VARCHAR(100) NOT NULL,
  value VARCHAR(100) NOT NULL,
  FOREIGN KEY (actividad_id) REFERENCES actividades(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS clientes (
  id INT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL UNIQUE,
  nombre_completo VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS proyectos (
  id INT PRIMARY KEY,
  nombre TEXT NOT NULL
);

