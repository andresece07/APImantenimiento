-- seeds_actividades.sql
USE mantenimiento;

-- Reiniciar tablas para evitar duplicados al ejecutar de nuevo
SET FOREIGN_KEY_CHECKS=0;
TRUNCATE TABLE posibles_respuestas;
TRUNCATE TABLE actividades;
SET FOREIGN_KEY_CHECKS=1;

--ACTIVIDADES PREVENTIVO
INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('Limpieza y organización de racks, equipos y ventiladores.', 'preventivo', 'single_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES
(@last_id, 'No fue necesario', 'no_necesario'), (@last_id, 'Muy Bien', 'muy_bien'), (@last_id, 'Bien', 'bien'),
(@last_id, 'Regular', 'regular'), (@last_id, 'Mal', 'mal'), (@last_id, 'Muy Mal', 'muy_mal');

INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('Aplicación y ejecución del protocolo de mantenimiento.', 'preventivo', 'single_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES
(@last_id, 'No fue necesario', 'no_necesario'), (@last_id, 'Muy Bien', 'muy_bien'), (@last_id, 'Bien', 'bien'),
(@last_id, 'Regular', 'regular'), (@last_id, 'Mal', 'mal'), (@last_id, 'Muy Mal', 'muy_mal');

INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('Solventar inconvenientes menores en caso de suscitarse o requerirlo.', 'preventivo', 'single_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES
(@last_id, 'No fue necesario', 'no_necesario'), (@last_id, 'Muy Bien', 'muy_bien'), (@last_id, 'Bien', 'bien'),
(@last_id, 'Regular', 'regular'), (@last_id, 'Mal', 'mal'), (@last_id, 'Muy Mal', 'muy_mal');

INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('Colocar etiqueta del mantenimiento correspondiente.', 'preventivo', 'single_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES
(@last_id, 'No fue necesario', 'no_necesario'), (@last_id, 'Muy Bien', 'muy_bien'), (@last_id, 'Bien', 'bien'),
(@last_id, 'Regular', 'regular'), (@last_id, 'Mal', 'mal'), (@last_id, 'Muy Mal', 'muy_mal');

INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('Peinado del cableado del equipo.', 'preventivo', 'single_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES
(@last_id, 'No fue necesario', 'no_necesario'), (@last_id, 'Muy Bien', 'muy_bien'), (@last_id, 'Bien', 'bien'),
(@last_id, 'Regular', 'regular'), (@last_id, 'Mal', 'mal'), (@last_id, 'Muy Mal', 'muy_mal');

INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('Verificar conexiones de datos y energía.', 'preventivo', 'single_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES
(@last_id, 'No fue necesario', 'no_necesario'), (@last_id, 'Muy Bien', 'muy_bien'), (@last_id, 'Bien', 'bien'),
(@last_id, 'Regular', 'regular'), (@last_id, 'Mal', 'mal'), (@last_id, 'Muy Mal', 'muy_mal');

INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('Verificar alarmas visuales externas.', 'preventivo', 'single_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES
(@last_id, 'No fue necesario', 'no_necesario'), (@last_id, 'Muy Bien', 'muy_bien'), (@last_id, 'Bien', 'bien'),
(@last_id, 'Regular', 'regular'), (@last_id, 'Mal', 'mal'), (@last_id, 'Muy Mal', 'muy_mal');

INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('Obtencion de Backup de configuracion del equipo.', 'preventivo', 'single_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES
(@last_id, 'No fue necesario', 'no_necesario'), (@last_id, 'Muy Bien', 'muy_bien'), (@last_id, 'Bien', 'bien'),
(@last_id, 'Regular', 'regular'), (@last_id, 'Mal', 'mal'), (@last_id, 'Muy Mal', 'muy_mal');

-- ACTIVIDADES CORRECTIVO
INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('Diagnóstico, verificación y solución problemas en forma remota.', 'correctivo', 'single_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES
(@last_id, 'No fue necesario', 'no_necesario'), (@last_id, 'Muy Bien', 'muy_bien'), (@last_id, 'Bien', 'bien'),
(@last_id, 'Regular', 'regular'), (@last_id, 'Mal', 'mal'), (@last_id, 'Muy Mal', 'muy_mal');

INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('Diagnóstico, verificación y solución problemas en sitio.', 'correctivo', 'single_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES
(@last_id, 'No fue necesario', 'no_necesario'), (@last_id, 'Muy Bien', 'muy_bien'), (@last_id, 'Bien', 'bien'),
(@last_id, 'Regular', 'regular'), (@last_id, 'Mal', 'mal'), (@last_id, 'Muy Mal', 'muy_mal');

INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('Traslado de los equipos para reparación correctiva.', 'correctivo', 'single_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES
(@last_id, 'No fue necesario', 'no_necesario'), (@last_id, 'Muy Bien', 'muy_bien'), (@last_id, 'Bien', 'bien'),
(@last_id, 'Regular', 'regular'), (@last_id, 'Mal', 'mal'), (@last_id, 'Muy Mal', 'muy_mal');

INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('Reemplazo de tarjetas o módulos ópticos.', 'correctivo', 'single_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES
(@last_id, 'No fue necesario', 'no_necesario'), (@last_id, 'Muy Bien', 'muy_bien'), (@last_id, 'Bien', 'bien'),
(@last_id, 'Regular', 'regular'), (@last_id, 'Mal', 'mal'), (@last_id, 'Muy Mal', 'muy_mal');

INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('Reemplazo de equipos.', 'correctivo', 'single_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES
(@last_id, 'No fue necesario', 'no_necesario'), (@last_id, 'Muy Bien', 'muy_bien'), (@last_id, 'Bien', 'bien'),
(@last_id, 'Regular', 'regular'), (@last_id, 'Mal', 'mal'), (@last_id, 'Muy Mal', 'muy_mal');

INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('En caso de ser necesario, instalar parche o upgrade del equipo.', 'correctivo', 'single_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES
(@last_id, 'No fue necesario', 'no_necesario'), (@last_id, 'Muy Bien', 'muy_bien'), (@last_id, 'Bien', 'bien'),
(@last_id, 'Regular', 'regular'), (@last_id, 'Mal', 'mal'), (@last_id, 'Muy Mal', 'muy_mal');

INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('Troubleshooting en el caso de configuraciones.', 'correctivo', 'single_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES
(@last_id, 'No fue necesario', 'no_necesario'), (@last_id, 'Muy Bien', 'muy_bien'), (@last_id, 'Bien', 'bien'),
(@last_id, 'Regular', 'regular'), (@last_id, 'Mal', 'mal'), (@last_id, 'Muy Mal', 'muy_mal');

INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('Verificar que el problema fue resuelto, agregar al informe.', 'correctivo', 'single_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES
(@last_id, 'No fue necesario', 'no_necesario'), (@last_id, 'Muy Bien', 'muy_bien'), (@last_id, 'Bien', 'bien'),
(@last_id, 'Regular', 'regular'), (@last_id, 'Mal', 'mal'), (@last_id, 'Muy Mal', 'muy_mal');

-- TAREAS DIAGNOSTICO
INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('Revision de estado por comandos esta sin alarmas en \"display alarm active | include Major\" (AR2504H) / \"display alarm active | include Major\"(S5720)', 'diagnostico', 'multiple_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES (@last_id, 'Realizado', 'realizado');

INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('Ejecucion de comando \"display health\" (AR2504H) / \"display environment\"ó \"displaytemperatureall\" (S5720) revisar que el campo STATUS este NORMAL ó CurrentTemperature debe estar entre los limites 0 a 60', 'diagnostico', 'multiple_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES (@last_id, 'Realizado', 'realizado');

INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('Ejecucion de comando \"display health\" (AR2504H) / \"display power\" (S5720) revisar que el campo STATE presente informacion de las fuentes de poder instaladas en el equipo ó que presente NORMAL', 'diagnostico', 'multiple_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES (@last_id, 'Realizado', 'realizado');

INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('Ejecucion de comando \"display health\" (AR2504H) / \"display fan verbose\" (S5720) revisar que el campo REGISTER presente informacion YES de los ventiladores que tengan los equipos ó que tenga status NORMA', 'diagnostico', 'multiple_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES (@last_id, 'Realizado', 'realizado');

INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('Ejecucion de comando \"display health\" (AR2504H) / \"display cpu-usage\" (S5720) revisar que el campo CPU USAGE presente informacion inferior a 80% en el equipo', 'diagnostico', 'multiple_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES (@last_id, 'Realizado', 'realizado');

INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('Ejecucion de comando \"display health\" (AR2504H) / \"display memory-usage\" (S5720) revisar que el campo USED PERCENTAGE de Memoria presente informacion inferior a 60% en el equipo', 'diagnostico', 'multiple_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES (@last_id, 'Realizado', 'realizado');

INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('Ejecucion de comando \"display health\" (AR2504H) / \"dir\" (S5720) revisar que el campo USED PERCENTAGE de Disco presente informacion inferior a 80% en el equipo ó al final revisar que el espacio libre en KB corresponda al 80%', 'diagnostico', 'multiple_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES (@last_id, 'Realizado', 'realizado');

INSERT INTO actividades (nombre, tipo, tipo_respuesta) VALUES ('Ejecucion de comando \"display device\" (AR2504H / S5720) revisar que las tarjetas esten con estados:', 'diagnostico', 'multiple_choice');
SET @last_id = LAST_INSERT_ID();
INSERT INTO posibles_respuestas (actividad_id, label, value) VALUES
(@last_id, 'Online es PRESENT.', 'online_es_present'), (@last_id, 'Power es POWERON.', 'power_es_poweron'),
(@last_id, 'Register es REGISTERED.', 'register_es_registered'), (@last_id, 'Alarm es NORMAL.', 'alarm_es_normal');