{% load i18n gravatartag %}
function commission (e) {
	e.preventDefault();
	var ctx = {
		"title": "{% trans 'Comisión aprobatoria' %}",
		"info_text": "{% trans 'Ésta Acta no será publicada a todo el grupo hasta que los miembros asignados como comisión aprobatoria estén de acuerdo con su redacción.' %}",
	}
	loadPanel(ctx, function () {
		loadPanelContent(swig.render($("#approvingCommissionTpl").html(),{locals: {} }));
		$(".popover-element").popover({trigger: 'hover'});
	});
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
		var params = {"annotation": t, "minutes_id": {{minutes.id}}}
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
	}else{
		setAlertError("{% trans 'Error' %}", "{% trans 'No puedes agregar una anotación vacía' %}")
	}
}
$(document).on("click", ".btn-no-approve", newAnnotation);
$(document).on("click", "#button-save", saveAnnotation);