{% load i18n gravatartag %}

function loadTasksPanel(e) {
	e.preventDefault();
	var ctx = {
		id: $(this).attr("id"),
		title: "{% trans 'Tareas' %}",
		info_text: "{% trans 'Organiza todas las tareas que requieras para cada acta' %}",
		callback: function () {
			sendNewAjax("{% url 'tasks:get_minutes_tasks' minutes.id %}",{}, function (data) {
				tasks = data
				loadPanelContent($('#taskManagerTpl').html());
				$('#taskAddBtn').on('click', function(){
						setTimeout(function(){
				            $("#taskName").focus();
				        }, 1);});
				tasks_html = swig.render($("#taskListTpl").html(),{locals: tasks })
				$('#tasksList').html(tasks_html)
				dp = $('.date-pick').datetimepicker({
				    format: 'YYYY-MM-DD',
				    pickTime: false,		            
				});
			});
		}
	}
	loadPanel(ctx);
}