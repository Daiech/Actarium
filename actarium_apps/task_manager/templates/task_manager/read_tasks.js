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
	        	console.log(data.form_errors)
				for (var i in data.form_errors){
					field_selector = "#"+i+"TaskForm"
					console.log(field_selector)
					$(field_selector).before( "<label class='error-form-task'>"+data.form_errors[i]+"</label>" );
		        } 
	        }
	        else if (data.error){
	        	setAlertError("{% trans 'Error' %}", data.error);
	        }
	        else if (data.successful){
	        	setAlertMessage("{% trans 'Tarea Agregada","Se ha agregado una nueva tarea al acta ' %} <strong>{{ minutes.code}}</strong> ");
	        	$("#taskDropdown").find(".close").click();
	        	cleanForm("#taskForm");
	        	cleanForm("#miniTaskForm");
	        	tasks = data.new_task
	        	tasks_html = swig.render($("#taskListTpl").html(),{locals: tasks })
				$('#tasksList').prepend(tasks_html)
	        }
        },
        {"method":"post"}
    );
}

function miniCreateTask(e){
	e.preventDefault();
  	e.stopPropagation();
  	console.log($("#miniNameTaskForm").val())
  	$("#nameTaskForm").val($("#miniNameTaskForm").val());
  	$("#newTaskBtn").click();
}

function setTaskDone(e){
	e.preventDefault();
  	e.stopPropagation();
  	task = $(this).closest(".one_task")[0];
  	task_id = $(task).attr("data-task-id");
  	sendNewAjax(
		"{% url 'tasks:set_task_done'%}",
		{"task_id":task_id},
		function (data) {
			if (data.error){
				setAlertError("{% trans 'Error' %}", data.error);
			}
			else if (data.successful){
				setAlertMessage("{% trans 'Tarea modiicada' %}", data.message);
				prev_task = $(task).prev()[0]
				tasks = data.new_task
	        	tasks_html = swig.render($("#taskListTpl").html(),{locals: tasks })
	        	$(task).remove()
				if (prev_task){
					$(prev_task).after(tasks_html)
				}
				else{
					$('#tasksList').prepend(tasks_html)
				}
			}
		}
	);
}


function setTaskCanceled(e){
	e.preventDefault();
  	e.stopPropagation();
  	task = $(this).closest(".one_task")[0];
  	task_id = $(task).attr("data-task-id");
  	sendNewAjax(
		"{% url 'tasks:set_task_canceled'%}",
		{"task_id":task_id},
		function (data) {
			if (data.error){
				setAlertError("{% trans 'Error' %}", data.error);
			}
			else if (data.successful){
				setAlertMessage("{% trans 'Tarea modiicada' %}", data.message);
				prev_task = $(task).prev()[0]
				tasks = data.new_task
	        	tasks_html = swig.render($("#taskListTpl").html(),{locals: tasks })
	        	$(task).remove()
				if (prev_task){
					$(prev_task).after(tasks_html)
				}
				else{
					$('#tasksList').prepend(tasks_html)
				}
			}
		}
	);
}

function editTask(e){
	$("#taskDropdown").css("display","block");
	task_id = $(this).attr("data-task-id");
	// console.log("task id antes de enviar",task_id)
  	sendNewAjax(
		"{% url 'tasks:get_task'%}",
		{"task_id":task_id},
		function (data) {
			if (data.error){
				setAlertError("{% trans 'Error' %}", data.error);
			}
			else if (data.successful){
				// prev_task = $(task).prev()[0]
				task = data.task[0]
	        	// console.log(task);
	        	$("#nameTaskForm").val(task.title);
	        	$("#descriptionTaskForm").val(task.description);
	        	$("option[value="+task.responsible_id+"] .responsible_option").attr("selected","selected");
	        	$("#dueTaskForm input").val(task.due)
	        	$("#taskId").val(task.id)
			}
		}
	);
}


$(document).on("submit","#taskForm", createTask)
$(document).on("submit","#miniTaskForm",miniCreateTask)
$(document).on("click",".set_task_done_btn", setTaskDone)
$(document).on("click",".set_task_canceled_btn", setTaskCanceled)
$(document).on("click",".one_task", editTask)