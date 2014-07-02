{% load i18n gravatartag %}

function loadTasksPanel(e) {
	e.preventDefault();
	var ctx = {
		id: $(this).attr("id"),
		title: "{% trans 'Tareas' %}",
		info_text: "{% trans 'Organiza todas las tareas que requieras para cada acta' %}",
		callback: function () {
			sendNewAjax("{% url 'tasks:get_minutes_tasks' minutes.id %}",{}, function (data) {
				console.log(data)
				tasks = data
				loadPanelContent($('#taskManagerTpl').html());
				tasks_html = swig.render($("#taskListTpl").html(),{locals: tasks })
				console.log(tasks_html)
				$('#tasksList').html(tasks_html)
				
				
			});
		}
	}
	loadPanel(ctx);
}

