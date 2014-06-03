{% ifequal is_form 1 %}
	function copyDate(){
		$(".date_mirror").empty().text(""+$("#id_date_start").val());
	}
	{% if not title_edit and not minutes_saved.error %} /*se esta No editando?*/
		function newMinutesText(){
			$("#id_agenda").val("<ol><li>Verificaci&oacute;n de qu&oacute;rum</li>"+
						"<li>Designaci&oacute;n de presidente y secretario de la reuni&oacute;n.</li>"+
						"<li>Lectura y aprobaci&oacute;n del orden del d&iacute;a.</li>"+
						"<li>Proposiciones y varios.</li>"+
						"<li>Nombramiento de la comisi&oacute;n aprobatoria del acta.</li>"+
		                "</ol>");

			$("#id_agreement").val("<ol><li>Se verific&oacute; la presencia del qu&oacute;rum estatutario para poder deliberar y decidir (53% del total de afiliados).</li>"+
							$("#assistance_hidden").html()+
							"<li>Designaci&oacute;n de presidente y secretario de la reuni&oacute;n.<br><br></li>"+
							"<li>Lectura y aprobaci&oacute;n del orden del d&iacute;a.<br><br></li>"+
							"<li>Proposiciones y varios.<br><br></li>"+
							"<li>Nombramiento de la comisi&oacute;n aprobatoria del acta.<br><br></li>"+
			                "</ol>");
		}
		newMinutesText();
	{% else %}
		$(".date_mirror").text(""+$("#first_date input").val());
	{% endif%}
	dp.change(function (e) {
		// console.log("HA CAMBIADO");
		copyDate();
	});

	$("#id_location").css('width','130px');
	$("#id_date_start").css('width','150px');
	$("#id_code").css('width','100px');
	$("#id_code_title").tooltip();
	// console.log("this is a form")
{% else %}
	$(".date_mirror").html(""+$("#minutes-container #first_date").text())
	// console.log("this is Not a form");
{% endifequal %}