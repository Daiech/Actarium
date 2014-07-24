{% load i18n gravatartag %}
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
