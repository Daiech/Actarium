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
					console.log(data);
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
						setAlertError("{% trans 'Error' %}", data.error);
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
	        if(data.errors){
	        	// console.log("ERRORES",data.errors)
				for (var i in data.errors){
					// console.log(i, data.errors[i])
					$( "#"+i+"TaskForm" ).before( "<label class='error-form-task'>"+data.errors[i]+"</label>" );
		        } 
	        }
	        else if (data.successful){
	        	setAlertMessage("Tarea Agregada","Se ha agregado una nueva tarea al acta <strong>{{ minutes.code}}</strong> ");
	        	$("#taskDropdown").find(".close").click();
	        	cleanForm("#taskForm");
	        	// console.log("NEW TASK",data.new_task)
	        	tasks = data.new_task
	        	tasks_html = swig.render($("#taskListTpl").html(),{locals: tasks })
				$('#tasksList').prepend(tasks_html)
	        }
        },
        {"method":"post"}
    );
}


$(document).on("submit","#taskForm", createTask)