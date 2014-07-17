{% load i18n gravatartag %}
function loadHistoryPanel(e) {
	e.preventDefault();
	var ctx = {
		"id": $(this).attr("id"),
		"title": "{% trans 'Historial de cambios' %}",
		"info_text": "{% trans 'Revisa todos los cambios que se han realizado en esta acta.' %}",
		"callback":  function () {
			loadPanelContent(swig.render($("#historyTpl").html(),{locals: {} }));
			$(".popover-element").popover({trigger: 'hover'});
		}
	}
	loadPanel(ctx);
}
versions = {
	{% for v in minutes_version %}
		"{{ v.id }}": {
			"id_minutes": "{{ v.id_minutesd }}",
			"id_user_creator": "{{ v.id_user_creator.get_full_name }}",
			"full_html": '{{ v.full_html|escapejs }}',
			"date_created": "{{ v.date_created }}",
		},
	{% endfor %}
}

function showVersion (e) {
	e.preventDefault();
	var version_id = $(this).attr("data-minutes-version");
	$("#minutes-version .version-date").empty().html(versions[version_id].date_created);
	$("#minutes-version .version-creator").empty().html(versions[version_id].id_user_creator);
	
	$("#minutes-version .diff_version").html(diff(versions[version_id].full_html, $("#minutes-container").html()));
	$("#minutes-version").show();
}

$(document).on("click", ".btn-minutes-version", showVersion);