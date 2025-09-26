USE mantenimiento;

INSERT IGNORE INTO roles (id, nombre) VALUES
(1, 'Tecnico de Campo'),
(2, 'Supervisor');

-- TTL de sesión: 1440 minutos (mínimo 24h)
INSERT IGNORE INTO parametros (clave, valor, tipo, descripcion)
VALUES ('sesion.ttl_minutos', '1440', 'int', 'Duración de la sesión en minutos (min 24h)');
