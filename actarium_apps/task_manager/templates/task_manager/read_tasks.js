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
				for (var i in data.form_errors){
					field_selector = "#"+i+"TaskForm";
					$(field_selector).before( "<label class='error-form-task'>"+data.form_errors[i]+"</label>" );
		        } 
	        }
	        else if (data.error){
	        	setAlertError("{% trans 'Error' %}", data.error);
	        }
	        else if (data.successful){
				if (data.task_updated){
					console.log("Update task")
					task_id = "#task"+data.new_task[0].id
					prev_task = $(task_id).prev()[0]
					tasks = data.new_task
		        	tasks_html = swig.render($("#taskListTpl").html(),{locals: tasks })
		        	$(task_id).remove()
					if (prev_task){
						$(prev_task).after(tasks_html)
					}
					else{
						$('#tasksList').prepend(tasks_html)
					}
				}
				else{
					tasks = data.new_task
		        	tasks_html = swig.render($("#taskListTpl").html(),{locals: tasks })
					$('#tasksList').prepend(tasks_html)	
				}
	        	setAlertMessage("Tarea",data.message);
	        	$("#taskDropdown").find(".close").click();
	        	cleanForm("#taskForm");
	        	cleanForm("#miniTaskForm");
	        }
        },
        {"method":"post"}
    );
}

function miniCreateTask(e){
	e.preventDefault();
  	e.stopPropagation();
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
				setAlertMessage("{% trans 'Tarea modificada' %}", data.message);
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

function setTaskAssigned(e){
	e.preventDefault();
  	e.stopPropagation();
  	task = $(this).closest(".one_task")[0];
  	task_id = $(task).attr("data-task-id");
  	sendNewAjax(
		"{% url 'tasks:set_task_assigned'%}",
		{"task_id":task_id},
		function (data) {
			if (data.error){
				setAlertError("{% trans 'Error' %}", data.error);
			}
			else if (data.successful){
				setAlertMessage("{% trans 'Tarea modificada' %}", data.message);
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
  	sendNewAjax(
		"{% url 'tasks:get_task'%}",
		{"task_id":task_id},
		function (data) {
			if (data.error){
				setAlertError("{% trans 'Error' %}", data.error);
			}
			else if (data.successful){
				task = data.task[0];
	        	$("#nameTaskForm").val(task.title);
	        	$("#descriptionTaskForm").val(task.description);
	        	$("#responsibleSelector option[value="+task.responsible_id+"]").attr("selected","selected")
	        	$("#dueTaskForm input").val(task.due)
	        	$("#taskId").val(task.id)
			}
		}
	);
}

function showDropDown(e){
	cleanForm("#taskForm");
	$("#taskId").val(0);
	$("#nameTaskForm").val($("#miniNameTaskForm").val());
}

function hideDropDown(e){
	e.preventDefault();
  	e.stopPropagation();
	cleanForm("#taskForm");
	$("#taskId").val(0);
	$("#taskDropdown").css("display","None");
}

function deleteTask(e){
	e.preventDefault();
  	e.stopPropagation();
  	if(window.confirm("{% trans '¿Estas seguro que deseas eliminar esta tarea?' %}")){
            task = $(this).closest(".one_task")[0];
		  	task_id = $(task).attr("data-task-id");
		  	sendNewAjax(
				"{% url 'tasks:delete_task'%}",
				{"task_id":task_id},
				function (data) {
					if (data.error){
						setAlertError("{% trans 'Error' %}", data.error);
					}
					else if (data.successful){
						setAlertMessage("{% trans 'Tarea eliminada' %}", data.message);
			        	$(task).remove();
					}
				}
			);
        } 
}


$(document).on("submit","#taskForm", createTask)
$(document).on("focus","#miniNameTaskForm",hideDropDown)
$(document).on("submit","#miniTaskForm",miniCreateTask)
$(document).on("click",".set_task_done_btn", setTaskDone)
$(document).on("click",".set_task_assigned_btn", setTaskAssigned)
$(document).on("click",".delete_task_btn", deleteTask)
$(document).on("click",".one_task", editTask)
$(document).on("click","#taskAddBtn",showDropDown)
$(document).on("click","#cancelBtn", hideDropDown)