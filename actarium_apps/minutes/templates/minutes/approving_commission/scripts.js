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
function editMinutesRoles (e) {
	e.preventDefault();
	var ctx = {
		"id": $(this).attr("id"),
		"title": "{% trans 'Roles de acta' %}",
		"info_text": "{% trans 'Ésta Acta no será publicada a todo el grupo hasta que los miembros asignados como comisión aprobatoria estén de acuerdo con su redacción.' %}",
		"callback":  function () {
			sendNewAjax("{% url 'minutes:get_approving_commission' group.slug minutes.id %}",{}, function (data){
				ctx = {
					members: {% if is_edit %}{{ members_list|safe }}{% else %}data.members{% endif %},
				}
				loadPanelContent(swig.render($("#editApprovingCommissionTpl").html(),{locals: ctx }));
				$(".popover-element").popover({trigger: 'hover'});
			});
		}
	}
	loadPanel(ctx);
}
function editCommission (e) {
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

/*annotations*/
function newAnnotation(e){
	e.preventDefault(e);
	tinyMCE.init({
        theme : "simple",
        mode : "textareas",
        height : "80",
        width : "100%",
        content_css : "{{ STATIC_URL }}js/vendor/tiny_mce/themes/simple/skins/default/editorstyles.css",
	});
	$("#new-annotation").removeClass("hidden");
	goToByScroll("#new-annotation", function(){
		$("#new-annotation textarea").focus();
		tinyMCE.get('textarea-new-annotation').focus();
	}
	);
}
function saveAnnotation(e){
	var username = "{{ user.get_full_name }}";
	var gravatar = "{{ user.email|showgravatar:'32'}}";
	var t = tinymce.get('textarea-new-annotation').getContent();
	if ( t.length > 1){
		/*
		USAR TEMPLATES: SWIG
		*/
		{% if minutes %}
		var params = {"annotation": t, "minutes_id": {{ minutes.id }}}
		sendNewAjax("/groups/{{group.slug}}/add-new-annotation",params, function(data){
				if(data){
					var m = '<div class="annotation bb">\
									<div class="user-gravatar pull-left">\
										<img class="size32 avatar" src="' + gravatar + '" alt="' + username + '" />\
									</div>\
									<div class="name-user-annotation">\
										<strong>' + username + '</strong>\
										· <time>Ahora mismo</time>\
									</div>\
									<div class="content-annotation">'+
										t +
									'</div>\
							</div>';
					$("#annotations").prepend("<li>" + m + "</li>");
					tinymce.get('textarea-new-annotation').setContent("");
				}
				else{
					setAlertError("Error", "Algo ocurri&oacute;");
				}
			},
			{"method": "post"}
		);
		{% endif %}
	}else{
		setAlertError("{% trans 'Error' %}", "{% trans 'No puedes agregar una anotación vacía' %}")
	}
}
if(window.location.hash){
	$(window.location.hash+" > div").addClass("selected-annontation");
}
$(document).on("click", ".btn-no-approve", newAnnotation);
$(document).on("click", "#button-save", saveAnnotation);
/*close annotations*/

/****roles for minutes ****/
function callBackApprove(data){
	$(".div-sign").fadeOut(300,function(){
		$(this).empty();
	});
	var u = $(".missing-"+data["user-id"]);
	if(data['approved']==1){
		u.find("div.icon-approver-status").html('<i class="glyphicon glyphicon-ok"></i>');
		setAlertMessage("{% trans 'Acta aprobada!' %}", "{% trans 'Haz aprobado esta acta' %}.");
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
	sendNewAjax(
		"{% url 'approve_minutes' %}",
		{"m_id":minutes_id, "approve": is_approved},
		callBackApprove,
		{"method": "post"}
	);
}
function isThereAprobers(e){
	var approvers = $(".approver").filter(':checked');
	if (approvers.length == 0){
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
	var role = checkbox.attr("data-role")
	var role_name = checkbox.attr("data-role-name")
	var uid = checkbox.attr("data-uid")
	var minutes_id = $("#minutesId").val();{% comment %}solo si se esta en edicion{% endcomment %}
	if(checkbox.is(":checked")){
		sendNewAjax("{% url 'set_minutes_role' group.slug %}",
			{"role":role, "uid": uid, "m_id": minutes_id, "remove": 0}, callbackSetRole,
			{"method": "post"})
	}
	else{
		sendNewAjax("{% url 'set_minutes_role' group.slug %}",
				{"role":role, "uid": uid, "m_id": minutes_id, "remove": 1}, callbackRemoveRole,
				{"method": "post"})
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
$(document).on("click", ".btn-approve", setApprove);
$(document).on("click", ".btn-send-notification .btn-cancel", cancelEditCommission);
$(document).on("click", ".set-role", setRole);//roles MAIN
$(document).on("change", "#sel-president", setPresident);//roles MAIN
$(document).on("change", "#sel-secretary", setSecretary);//roles MAIN
$(document).on('change', "#show-dni", setShowDNI);
$(document).on('click', ".btn-next", isThereAprobers);
$(document).on('click', "#btnEditCommission", editCommission);

/****close roles for minutes ****/
