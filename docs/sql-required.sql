-- this data is required to run actarium.

INSERT INTO `actions_log_actions` (`id`, `name`, `code`, `description`) VALUES
(1, 'Iniciar sesión', 'LOG_IN', 'Un usuario inicia sesión en la plataforma.'),
(2, 'Registro de usuarios', 'SIGN_IN', 'Acción de registrar un usuario en la plataforma.'),
(3, 'Cerrar sesión', 'LOG_OUT', 'Acción de cerrar sesion, solo se ejecuta cuando se da clic en el botón "cerrar sesión" no cuando cierran el navegador o apagan el computador'),
(4, 'Nueva reunión', 'NEW_REUNION', 'Convocación de una reunión, se almacena el id de la reunión y el grupo al que pertenece.'),
(5, 'Nueva acta', 'NEW_MINUTE', 'Creación de una nueva acta, guarda el grupo al que pertenece y su codigo correpondiente.'),
(6, 'Confirmar asistencia', 'SET_ASSIST', 'Confirmara asistencia indicando el id de la reunión y el valor, True: aceptar y False: rechazar'),
(7, 'Nuevo Grupo', 'NEW_GROUP', 'Creación de un nuevo grupo, guarda el nombre del grupo y el nombre del administrador'),
(8, 'Aceptar invitación', 'SET_INVITA', 'Acción de aceptar o rechazar una invitación a un grupo'),
(9, 'Eliminar invitación', 'DEL_INVITA', 'Elimina la invitación que se ha hecho a un usuario para participar en un grupo'),
(10, 'Actualizar datos', 'CHG_USDATA', 'Actualizar datos de usuario, se guarda la información anterior del usuario'),
(11, 'Cambiar Contraseña', 'CHG_PASS', 'Notificación de cambio de contraseña'), 
(12, 'Enviar Invitación', 'SEN_INVITA', 'Acción de enviar invitación a participar en un grupo, guarda el email al cual se envio la invitación.'),
(13, 'Nueva organizacion', 'NEW_ORG', 'Crear nueva organizacion'),
(14, 'Editar organización', 'EDIT_ORG', 'Editar organizacion');


INSERT INTO `groups_minutes_type` (`id`, `name`, `description`, `id_creator_id`, `is_public`, `is_customized`) VALUES
(1, 'Reunión', 'Formato de acta para reuniones', 1, 1, 0),
(2, 'Last Minutes', 'Formato de acta para reuniones', 1, 1, 0);


INSERT INTO `groups_group_type` (`id`, `name`, `description`) VALUES
(1, 'Reunión', 'Tipo de grupo que se reúne para tomar decisiones.'),
(2, 'Junta Directiva', 'junta directiva de cualquier organización'),
(3, 'Comité', 'Grupo para las reuniones de comité'),
(4, 'Proyecto', 'Grupo para las reuniones de proyectos');


INSERT INTO `groups_packages` (`id`, `name`, `number_groups_pro`, `price`, `is_visible`, `date_joined`,`time`) VALUES
(1, 'Grupo Pro Individual', 1, '6000', 1, '2013-01-31 21:00:12',6),
(2, 'Promoción Pro x3', 3, '16000', 1, '2013-01-31 20:59:28',12),
(3, 'Promoción Pro x6', 6, '30000', 1, '2013-01-31 20:58:12',12);


INSERT INTO `groups_templates` (`id`, `name`, `address_template`, `address_js`, `id_type_id`, `is_public`, `date_joined`, `slug`) VALUES
(1, 'basica', 'groups/minutesTemplates/minutesTemplate1.html', 'groups/minutesTemplates/minutesTemplate1js.html', 1, 1, '2013-03-15 02:37:31', 'basica-1'),
(2, 'Asamblea General Parquesoft Pereira', 'groups/minutesTemplates/minutesTemplate2.html', 'groups/minutesTemplates/minutesTemplate2js.html', 1, 0, '2013-03-15 01:04:51', 'asamblea-general-parquesoft-pereira-2'),
(3, 'Comité Parquesoft Pereira', 'groups/minutesTemplates/minutesTemplate3.html', 'groups/minutesTemplates/minutesTemplate3js.html', 1, 0, '2013-03-15 02:37:57', 'comite-parquesoft-pereira-3'),
(4, 'Actas subidas', 'groups/minutesTemplates/minutesTemplate4.html', 'groups/minutesTemplates/minutesTemplateJsEmpty.html', 2, 0, '2013-03-15 13:55:52', 'actas-subidas-4');


INSERT INTO `website_globalvars` (`id`, `name`, `url`, `description`, `date_created`) VALUES
(1, 'URL_TERMS', 'terminos-y-condiciones-de-uso', 'Url de los términos y condiciones', '2013-03-23 19:22:44'),
(2, 'URL_PRIVACY', 'politicas-de-privacidad', 'Url de las politicas-de-privacidad', '2013-03-23 19:55:08');



INSERT INTO `emailmodule_email_admin_type` (`id`, `name`, `description`, `date_added`) VALUES
(1, 'obligatorio', 'Este tipo de correos son obligatorios y no se pueden desactivar', '2013-07-25 04:14:29'),
(2, 'grupo', 'Este tipo de correo esta directamente ligado a un grupo, el la configuración de cada grupo se pueden desactivar', '2013-07-25 04:15:09'),
(3, 'global', 'Este tipo de correo esta relacionado directamente con cada usuario y se pueden desactivar o activar en las configuraciones generales', '2013-07-25 04:16:08'),
(4, 'staff', 'Correo que se envía al staff de Actarium', '2013-07-25 04:47:20');


INSERT INTO `emailmodule_email` (`id`, `name`, `description`, `email_type`, `admin_type_id`, `date_added`) VALUES
(1, 'validación de correo', 'Correo de validacion para activar la cuenta', '1', 1, '2013-07-25 04:27:45'),
(2, 'Nueva reunion', 'Correo que indica cuando un usuario invita a otro a una reunion', '2', 2, '2013-07-25 04:28:22'),
(3, 'Nueva acta', 'Correo que informa a un usuario cuando se ha creado una nueva acta en un grupo', '3', 2, '2013-07-25 04:28:58'),
(4, 'Asignacion de rol', 'Correo que informa a un usuario cuando le han asignado un rol dentro de un grupo', '4', 2, '2013-07-25 04:29:46'),
(5, 'Confirmacion de asistencia a reunion', 'Correo que informa al convocador de una reunion cuando alguien responde a dicha reunion afirmativa o negativamente', '5', 2, '2013-07-25 04:30:49'),
(6, 'Invitacion a un grupo', 'Correo que llega a un usuario cuando alguien lo invita a hacer parte de un grupo', '6', 3, '2013-07-25 04:31:41'),
(7, 'Invitacion a Actarium', 'Correo que se envia cuando un usuario invita a otra persona a usar Actarium', '7', 1, '2013-07-25 04:32:56'),
(8, 'Respuesta de invitacion a grupo', 'Cuando un usuario responde a la solicitud de hacer parte de un grupo, se envía un correo a la persona que realizo dicha invitación.', '8', 2, '2013-07-25 04:34:45'),
(9, 'feedback', 'Comentarios que dejan los usuarios, se envia directamente al staff de Actarium', '9', 4, '2013-07-25 04:50:10'),
(10, 'resend_activate_account', 'email_resend_activate_account', '10', 3, '2013-07-25 04:50:10'),
(11, 'group_reinvitation', 'email_group_reinvitation', '11', 2, '2013-07-25 04:50:10'),
(12, 'new_annotation', 'email_new_annotation', '12', 2, '2013-07-25 04:50:10'),
(13, 'new_minutes_for_approvers', 'email_new_minutes_for_approvers', '13', 2, '2013-07-25 04:50:10'),
(14, 'dni group', 'Correo de solicitud de acceso a DNI para un grupo', '14', 2, '2013-07-25 04:50:10');
