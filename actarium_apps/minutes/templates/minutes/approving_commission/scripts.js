{% load i18n gravatartag %}
function showCommission (e) {
	e.preventDefault();
	var ctx = {
		"id": $(this).attr("id"),
		"title": "{% trans 'Comisión aprobatoria' %}",
		"info_text": "{% trans 'Ésta Acta no será publicada a todo el grupo hasta que los miembros asignados como comisión aprobatoria estén de acuerdo con su redacción.' %}",
		"callback":  function () {
			sendNewAjax("{% url 'minutes:get_approving_commission' group.slug minutes.id %}",{}, function (data){
				approve = $.grep(data.members, function (element, index) {return element.id == "{{ user.id }}" && element.role.is_approver});
				i_have_approved = $.grep(data.members, function (element, index) {return element.id == "{{ user.id }}" && element.role.is_approver && element.get_minutes_signed != 0});
				ctx = {ca: data.members, i_should_approve: approve.length, i_have_approved: i_have_approved.length};
				loadPanelContent(swig.render($("#approvingCommissionTpl").html(),{locals: ctx }));
				$(".popover-element").popover({trigger: 'hover'});
			});
		}
	}
	loadPanel(ctx);
}
function editMinutesRoles (e) { {% comment %}Se ejecuta cuando se edita un acta, o solo la comision{% endcomment %}
	e.preventDefault();
	var is_edit = "{{ is_edit }}";
	var ctx = {
		"id": $(this).attr("id"),
		"title": "{% trans 'Roles de acta' %}",
		"info_text": "{% trans 'Ésta Acta no será publicada a todo el grupo hasta que los miembros asignados como comisión aprobatoria estén de acuerdo con su redacción.' %}",
		"callback":  function () {
			sendNewAjax("{% url 'minutes:get_approving_commission' group.slug minutes.id %}",{}, function (data){
				ctx = {
					// members: {% if is_edit %}{{ members_list|safe }}{% else %}data.members{% endif %},
					members: data.members,
				}
				loadPanelContent(swig.render($("#editApprovingCommissionTpl").html(),{locals: ctx }));
				$(".popover-element").popover({trigger: 'hover'});
				console.log(ctx);
			});
		}
	}
	loadPanel(ctx);
}
function editCommission (e) { {% comment %}se ejecuta cuando solo se edita la comision (no el acta){% endcomment %}
	e.preventDefault();
	var ctx = {
		"id": $(this).attr("id"),
		"title": "{% trans 'Editar comisión aprobatoria' %}",
		"info_text": "{% trans 'Solo puedes editar la comisíón aprobatoria. Para editar otro dato debes editar el acta completa.' %}",
		"callback":  function () {
			sendNewAjax("{% url 'minutes:get_approving_commission' group.slug minutes.id %}",{}, function (data){
				var president = $.grep(data.members, function (element, index) {return element.role.is_president;});
				var secretary = $.grep(data.members, function (element, index) {return element.role.is_secretary;});
				if ( president.length > 0 ) {president = president[0].short_name[0]}else{president = "{% trans 'Noy hay presidente' %}"}
				if ( secretary.length > 0 ) {secretary = secretary[0].short_name[0]}else{secretary = "{% trans 'Noy hay secretario' %}"}
				ctx = {
					members: data.members,
					president: president,
					secretary: secretary,
					commission_is_editing: true}
				loadPanelContent(swig.render($("#editApprovingCommissionTpl").html(),{locals: ctx }));
				$(".popover-element").popover({trigger: 'hover'});
			});
		}
	}
	loadPanel(ctx);
}

/****roles for minutes ****/
function callBackApprove(data){
	if(data['approved']==1){
		setAlertMessage("{% trans 'Acta aprobada!' %}", "{% trans 'Haz aprobado esta acta' %}.");
		$(".div-sign").fadeOut(300,function(){
			$(this).empty();
			var u = $(".missing-"+data["user-id"]);
			u.find(".remember-approve").hide().remove();
			icon = u.find(".icon-approver-status .glyphicon-time");
			icon.removeClass("glyphicon-time").removeClass("popover-element").addClass("glyphicon-ok");
			icon.attr("data-content", "{% trans 'aprobó esta acta' %}")
		});
		if (data["is_full_signed"]){
			$("#minutes-edit").closest("li").fadeOut("fast");
			$("#btn-generate-pdf").removeClass("disabled").attr("data-original-title","{% trans 'Descarga esta acta en PDF' %}").on("click", function (e) {e.preventDefault();$("#pdf-form").submit();});
		}
	}
}
function setApprove(e){
	e.preventDefault();
	$(this).attr({"disabled": "disabled"});
	var minutes_id = $(this).attr("data-minutes");
	var is_approved = parseInt($(this).attr("data-approve"));
	console.log('se esta ejecutando setApprove de scripts.js')
	var badge_quantity = parseInt($('#list_pending_approval_of_minutes .badge').html())
	$('#list_pending_approval_of_minutes .badge').html(badge_quantity-1)
	var summary_quantity = parseInt($('#notification-summary-dropdown .notification-summary-badge').html())
	$('#notification-summary-dropdown .notification-summary-badge').html(summary_quantity-1)
	sendNewAjax(
		"{% url 'approve_minutes' %}",
		{"m_id":minutes_id, "approve": is_approved},
		callBackApprove,
		{"method": "post"}
	);
}
function isThereAprobers(e){
	return is_one_selected(e, ".approver");
}
function isThereAttendees(e){
	return is_one_selected(e, ".attendees");
}
function is_one_selected (e, elem) {
	var checkbox = $(elem).filter(':checked');
	if (checkbox.length == 0){
		e.preventDefault();
		e.stopPropagation();
		return false;
	}
	else{
		return true;
	}
}

function addMemberToList (user) {
	$("#minutes .empty-list").empty();
	$("#minutes .members-list").append("<li>"+ user.full_name + "</li>")
}
function removeMemberToList (user) {
	$("#minutes .members-list").find(".member-" + user.id).remove();
}
function getRoleName (op) {
	switch(op){
		case 1 : return "{% trans 'Administrador de éste grupo' %}"; break;
		case 2 : return "{% trans 'Aprobador de actas' %}"; break;
		case 3 : return "{% trans 'Redactor (Puede redactar Actas)' %}"; break;
	}
}
function callbackSetRole(data) {
	if (data["saved"]){
    	// setAlertMessage("Rol agregado", data['u'] + " ahora es " + data['role_name'] + " del acta a crear.")
		if (data.role === 3){
			addMemberToList({"id": data.uid, "username": data.username, "first_name": data.u, "full_name": data.full_name});
		}
		else{
			// console.log("es", data.role_name);
		}
    }
    else{
    	setAlertError("{% trans 'Ocurrió un error' %}", data['error'])
    }
}
function callbackRemoveRole(data) {
	if (data["saved"]){
    	// setAlertMessage("Rol removido", data['u'] + " ya no es " + data['role_name'] + " del acta a crear.")
    	if (data.role === 3){
			removeMemberToList({"id": data.uid, "username": data.username, "first_name": data.u, "full_name": data.full_name});
		}
    }
    else{
    	setAlertError("{% trans 'Ocurrió un error' %}", data['error'])
    }
}
function setRole(e) {
	var checkbox = $(this);
	var role = checkbox.attr("data-role");
	var role_name = checkbox.attr("data-role-name");
	var uid = checkbox.attr("data-uid");
	var minutes_id = $("#minutesId").val();{% comment %}solo si se esta en edicion{% endcomment %}
	if(checkbox.is(":checked")){
		sendNewAjax("{% url 'set_minutes_role' group.slug %}",
			{"role":role, "uid": uid, "m_id": minutes_id, "remove": 0}, callbackSetRole,
			{"method": "post"});
	}
	else{
		sendNewAjax("{% url 'set_minutes_role' group.slug %}",
				{"role":role, "uid": uid, "m_id": minutes_id, "remove": 1}, callbackRemoveRole,
				{"method": "post"});
	}
}
function callbackSetPresident (data) {
	if (data["saved"]){
    	setAlertMessage("Rol agregado", data['u'] + " ahora es " + data['role_name'] + " del acta a crear.")
		$(".president-ok").removeClass("hidden");
		//show all options for to set a secretary
		$("#sel-secretary option").show();
		//hide the president in the secretary select
		$("#sel-secretary option[value=" + data['uid'] +"]").hide();
		//Put checked the President checkbox: approver & signer
		// $("#signer"+data['uid']).attr("disabled","disabled");
    }
    else{
    	setAlertError("Ocurri&oacute; un error", data['error'])
    	$("#sel-president").val(0);
    }
}
function callbackSetSecretary (data) {
	if (data["saved"]){
    	setAlertMessage("Rol agregado", data['u'] + " ahora es " + data['role_name'] + " del acta a crear.")
		$(".secretary-ok").removeClass("hidden");
		$("#sel-president option").show();
		$("#sel-president option[value=" + data['uid'] +"]").hide();
		// $("#signer"+data['uid']).attr("disabled","disabled");
    }
    else{
    	setAlertError("Ocurri&oacute; un error", data['error']);
    	$("#sel-secretary").val(0);
    }
}
function setPresident (e) {
	$(".president-ok").addClass("hidden");
	var uid = $(this).val();
	var minutes_id = $("#minutesId").val();
	sendNewAjax("{% url 'set_minutes_role' group.slug %}",
		{"role":4, "uid": uid, "m_id": minutes_id,  "remove": 0}, callbackSetPresident,
			{"method": "post"}
	);
}
function setSecretary (e) {
	$(".secretary-ok").addClass("hidden");
	var uid = $(this).val();
	var minutes_id = $("#minutesId").val();
	sendNewAjax("{% url 'set_minutes_role' group.slug %}",
		{"role":5, "uid": uid, "m_id": minutes_id,  "remove": 0}, callbackSetSecretary,
			{"method": "post"}
	);
}
function setShowDNI(e){
	sendAjax("/groups/{{group.slug}}/set-show-dni",
		{},"", 
		function(data){
			if (data["saved"]){
		    	setAlertMessage("Configuraci&oacute;n realizada", "Se ha guardado correctamente la configuraci&oacute;n de visualizaci&oacute;n de DNI en las actas")
		    }
		    else{
		    	setAlertError("Ocurri&oacute; un error", data['error'])
		    }
		}
	);
}
function cancelEditCommission(e){
	e.preventDefault();
	$("#commissionPanel").click();
}
function sendEmailToApprovers(e){
	e.preventDefault();
	{% if minutes %}
	sendNewAjax(
		"{% url 'email_to_approvers' group.slug minutes.id %}",
		{},
		function (data) {
			if (data.sent){
				setAlertMessage("{% trans 'Correo enviado' %}", "{% trans 'Se ha enviado un correo de notificación a quienes no han aprobado el acta.' %}")
			}
		}
	);
	{% endif %}
	$("#commissionPanel").click();
}
function rememberApprove(e){
	e.preventDefault();
	var uid = $(this).attr("data-uid");
	{% if minutes %}
	sendNewAjax("{% url 'email_to_approver' group.slug minutes.id %}",{uid: uid}, function(data){
		if (data.sent){
			setAlertMessage("{% trans 'Recordatorio enviado' %}", data.msj);
		}else{
			setAlertError("{% trans 'Recordatorio NO enviado' %}", data.msj);
		}
	},{"method":"post"});
	{% endif %}
}
$(document).on("click", ".btn-approve", setApprove);
$(document).on("click", ".remember-approve", rememberApprove);
$(document).on("click", "#sendEmailToApprovers", sendEmailToApprovers);
$(document).on("click", ".btn-send-notification .btn-cancel", cancelEditCommission);
$(document).on("click", ".set-role", setRole);//roles MAIN
$(document).on("change", "#sel-president", setPresident);//roles MAIN
$(document).on("change", "#sel-secretary", setSecretary);//roles MAIN
$(document).on('change', "#show-dni", setShowDNI);
$(document).on('click', ".btn-next", isThereAprobers);
$(document).on('click', "#btnEditCommission", editCommission);

/****close roles for minutes ****/
