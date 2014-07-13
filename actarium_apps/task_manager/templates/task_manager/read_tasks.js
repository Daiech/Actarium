{% load i18n gravatartag %}

function loadTasksPanel(e) {
	e.preventDefault();
	var ctx = {
		id: $(this).attr("id"),
		title: "{% trans 'Tareas' %}",
		info_text: "{% trans 'Organiza todas las tareas que requieras para cada acta' %}",
		callback: function () {
			sendNewAjax({% if minutes %}
				"{% url 'tasks:get_minutes_tasks' minutes.id %}",
				{% else %}
				"{% url 'tasks:get_minutes_tasks' 0 %}",
				{% endif %}{},
				function (data) {
					if (!data.error){
						tasks = data;
						loadPanelContent($('#taskManagerTpl').html());
						$('#taskAddBtn').on('click', function(){
								setTimeout(function(){
						            $("#nameTaskForm").focus();
						        }, 1);});
						tasks_html = swig.render($("#taskListTpl").html(),{locals: tasks })
						$('#tasksList').html(tasks_html);
						dp = $('.date-pick').datetimepicker({
						    format: 'YYYY-MM-DD',
						    pickTime: false,		            
						});
					}
					else{
						// setAlertError("{% trans 'Error' %}", data.error);
						loadPanelContent($("#taskEmptyTpl").html());
					}
				});
		}
	}
	loadPanel(ctx);
}


function createTask(e) {
  	e.preventDefault();
  	e.stopPropagation();
  	$('.error-form-task').remove();
  	sendNewAjax(
        "{% url 'tasks:create_task' %}",
        $(this).serialize(),
        function (data) {
	        if(data.form_errors){
				for (var i in data.errors){
					$( "#"+i+"TaskForm" ).before( "<label class='error-form-task'>"+data.errors[i]+"</label>" );
		        } 
	        }
	        else if (data.error){
	        	setAlertError("{% trans 'Error' %}", data.error);
	        }
	        else if (data.successful){
	        	setAlertMessage("Tarea Agregada","Se ha agregado una nueva tarea al acta <strong>{{ minutes.code}}</strong> ");
	        	$("#taskDropdown").find(".close").click();
	        	cleanForm("#taskForm");
	        	tasks = data.new_task
	        	tasks_html = swig.render($("#taskListTpl").html(),{locals: tasks })
				$('#tasksList').prepend(tasks_html)
	        }
        },
        {"method":"post"}
    );
}


$(document).on("submit","#taskForm", createTask)