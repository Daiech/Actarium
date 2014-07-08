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
				            $("#nameTaskForm").focus();
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


function createTask(e) {
  	e.preventDefault();
  	e.stopPropagation();
  	$('.error-form-task').remove();
  	sendNewAjax(
        "{% url 'tasks:create_task' %}",
        $(this).serialize(),
        function (data) {
	        if(data.errors){
	        	console.log("ERRORES",data.errors)
				for (var i in data.errors){
					console.log(i, data.errors[i])
					$( "#"+i+"TaskForm" ).before( "<label class='error-form-task'>"+data.errors[i]+"</label>" );
		        } 
	        }
	        else if (data.successful){
	        	setAlertMessage("Tarea Agregada","Se ha agregado una nueva tarea al acta <strong>{{ minutes.code}}</strong> ");
	        	$("#taskDropdown").find(".close").click();
	        	cleanForm("#taskForm");
	        }
        },
        {"method":"post"}
    );
}


$(document).on("submit","#taskForm", createTask)