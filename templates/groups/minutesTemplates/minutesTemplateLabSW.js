{% ifequal is_form 1 %}	
	{% if not title_edit and not minutes_saved.error %}
	function newMinutesText(){
		$("#id_agenda").val("<ol><li>Tema</li>"+
					"<li>Objetivo de la reuni&oacute;n</li>"+
					"<li>Desarrollo de la reuni&oacute;n</li>"+
					"<ol><li>Temas a tratar</li>"+
					"<li>Seguimiento tareas acta anterior (Agregar link)</li>"+
					"<li>Desarrollo de los temas</li>"+
					"<li>Anexos</li></ol>"+
					"<li>Tareas pendientes / compromisos / pol&iacute;ticas </li>"+
					"<li>Observaciones</li>"+
	                "</ol>");
	
		$("#id_agreement").val("<ol><li>&nbsp;</li>"+
						"<li>&nbsp;</li>"+
						"<li>&nbsp;</li>"+
						"<ol><li>&nbsp;</li>"+
						"<li>&nbsp;</li>"+
						"<li>&nbsp;</li>"+
						"<li>&nbsp;</li></ol>"+
						"<li>&nbsp;</li>"+
						"<li>&nbsp;</li>"+
		                "</ol>");
	}
			
	newMinutesText();
	{% endif %}
{% endifequal%}