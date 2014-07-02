{% load i18n gravatartag %}
function showCommission (e) {
	e.preventDefault();
	var ctx = {
		"id": $(this).attr("id"),
		"title": "{% trans 'Comisión aprobatoria' %}",
		"info_text": "{% trans 'Ésta Acta no será publicada a todo el grupo hasta que los miembros asignados como comisión aprobatoria estén de acuerdo con su redacción.' %}",
		"callback":  function () {
			loadPanelContent(swig.render($("#approvingCommissionTpl").html(),{locals: {} }));
			$(".popover-element").popover({trigger: 'hover'});
		}
	}
	loadPanel(ctx);
}
function editCommission (e) {
	e.preventDefault();
	var ctx = {
		"id": $(this).attr("id"),
		"title": "{% trans 'Roles de acta' %}",
		"info_text": "{% trans 'Ésta Acta no será publicada a todo el grupo hasta que los miembros asignados como comisión aprobatoria estén de acuerdo con su redacción.' %}",
		"callback":  function () {
			sendNewAjax("{% url 'minutes:get_approving_commission' group.slug %}",{}, function (data){
				ctx = {
					members: data.members,
					name: "nhommasdf"
				}
				loadPanelContent(swig.render($("#editApprovingCommissionTpl").html(),{locals: ctx }));
			});
			$(".popover-element").popover({trigger: 'hover'});
		}
	}
	loadPanel(ctx);
}
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
$(document).on("click", ".btn-approve", setApprove);

if(window.location.hash){
	$(window.location.hash+" > div").addClass("selected-annontation");
}
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
$(document).on("click", ".btn-no-approve", newAnnotation);
$(document).on("click", "#button-save", saveAnnotation);



function callbackSetRole(data) {
	if (data["saved"]){
    	setAlertMessage("Rol agregado", data['u'] + " ahora es " + data['role'] + " del acta a crear.")
    }
    else{
    	setAlertError("Ocurri&oacute; un error", data['error'])
    }
}
function callbackRemoveRole(data) {
	if (data["saved"]){
    	setAlertMessage("Rol removido", data['u'] + " ya no es " + data['role'] + " del acta a crear.")
    }
    else{
    	setAlertError("Ocurri&oacute; un error", data['error'])
    }
}


/****roles for minutes ****/


function isThereAprobers(e){
	console.log('enter to  isThereAprobers');
	approvers = $(".approver").filter(':checked');
	if (approvers.length == 0){
		e.preventDefault();
		e.stopPropagation();
		setAlertMessage("Se necesta aprobador", "Es necesario que se defina por lo menos un miembro del equipo como aprobador del acta")
	}
}

function getRoleName (op) {
	switch(op){
		case 1 : return "Administrador de &eacute;ste grupo"; break;
		case 2 : return "Aprobador de actas"; break;
		case 3 : return "Redactor (Puede redactar Actas)"; break;
	}
}
function callbackSetRole(data) {
	if (data["saved"]){
    	setAlertMessage("Rol agregado", data['u'] + " ahora es " + data['role'] + " del acta a crear.")
    }
    else{
    	setAlertError("Ocurri&oacute; un error", data['error'])
    }
}
function callbackRemoveRole(data) {
	if (data["saved"]){
    	setAlertMessage("Rol removido", data['u'] + " ya no es " + data['role'] + " del acta a crear.")
    }
    else{
    	setAlertError("Ocurri&oacute; un error", data['error'])
    }
}
function setRole(e) {
	var checkbox = $(this);
	var role = checkbox.attr("data-role")
	var role_name = checkbox.attr("data-role-name")
	var uid = checkbox.attr("data-uid")
	// console.log(checkbox.is(":checked"));
	if(checkbox.is(":checked")){
		sendAjax("/groups/{{group.slug}}/set-rol-for-minute",
			{"role":role, "uid": uid, "remove": 0},"",callbackSetRole)
	}
	else{
		// if(confirm("{% trans 'Seguro que desea remover esta característica?' %}")){
		// }
		// else{
		// 	checkbox.attr("checked","checked")
		// }
		sendAjax("/groups/{{group.slug}}/set-rol-for-minute",
				{"role":role, "uid": uid, "remove": 1},"",callbackRemoveRole)
	}
}
function callbackSetPresident (data) {
	if (data["saved"]){
    	setAlertMessage("Rol agregado", data['u'] + " ahora es " + data['role'] + " del acta a crear.")
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
    	setAlertMessage("Rol agregado", data['u'] + " ahora es " + data['role'] + " del acta a crear.")
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
	$(".president-ok").addClass("hidden")
	var uid = $(this).val();
	sendAjax("/groups/{{group.slug}}/set-rol-for-minute",
		{"role":4, "uid": uid, "remove": 0},"",callbackSetPresident)
}
function setSecretary (e) {
	$(".secretary-ok").addClass("hidden")
	var uid = $(this).val();
	sendAjax("/groups/{{group.slug}}/set-rol-for-minute",
		{"role":5, "uid": uid, "remove": 0},"",callbackSetSecretary)
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
$(document).on("click", ".set-role", setRole);//roles MAIN
$(document).on("change", "#sel-president", setPresident);//roles MAIN
$(document).on("change", "#sel-secretary", setSecretary);//roles MAIN
$(document).on('change', "#show-dni", setShowDNI);
$(document).on('click', ".btn-next", isThereAprobers);

/****close roles for minutes ****/
