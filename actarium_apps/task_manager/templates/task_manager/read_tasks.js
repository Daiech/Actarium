{% load i18n gravatartag %}
var me = {{ request.user.id }};
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
					$("#taskDropdown").css({'overflow-y':"scroll"}).find(".dropdown-body").height($(window).height()-200)
				});
		}
	}
	loadPanel(ctx);
}

function createTask(e) {
  	e.preventDefault();
  	e.stopPropagation();
  	console.log($(this),$(this).serialize())
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
  	cleanForm("#taskForm");
  	$("#accountableSelector option[value='']").attr("selected",true)
  	$("#responsibleSelector option[value="+me+"]").attr("selected","selected")
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

function showTask(e){
	task_id = $(this).attr("data-task-id");
  	sendNewAjax(
		"{% url 'tasks:get_task'%}",
		{"task_id":task_id},
		function (data) {
			if (data.error){
				setAlertError("{% trans 'Error' %}", data.error);
			}
			else if (data.successful){
				task = data.task[0]
        		task_html = swig.render($("#taskModal").html(),{locals: task })
        		console.log('con',task.consulted)
        		$("#minutesModal").html(task_html);
        		$("#minutesModal").modal();
			}
		}
	);
}

function editTask(e){
	e.preventDefault();
  	e.stopPropagation();
	task_id = $(this).attr("data-task-id");
	console.log('tarea id',task_id)
  	sendNewAjax(
		"{% url 'tasks:get_task'%}",
		{"task_id":task_id},
		function (data) {
			if (data.error){
				setAlertError("{% trans 'Error' %}", data.error);
			}
			else if (data.successful){
				if (data.task[0].status_code != "TER"){
					cleanForm("#taskForm");
		        	task = data.task[0];
		        	console.log(task);
		        	//data of fields
		        	$("#nameTaskForm").val(task.title);
		        	$("#descriptionTaskForm").val(task.description);
		        	$("#responsibleSelector option[value="+task.responsible_id+"]").attr("selected","selected")
		        	
		        	if (task.accountable) {
		        		$("#accountableSelector option[value="+task.accountable.id+"]").attr("selected","selected")
		        	}
		        	else{
		        		$("#accountableSelector option[value='']").attr("selected",true)	
		        	}
		        	$("#dueTaskForm input").val(task.due)
		        	$.each(task.consulted, function(i,e){
					    $("#consultedSelector option[value='" + e.id + "']").prop("selected", true);
					});
		        	$.each(task.informed, function(i,e){
					    $("#informedSelector option[value='" + e.id + "']").prop("selected", true);
					});

		        	$("#taskId").val(task.id)
		        	$("#taskDropdown").css("display","block");
		        }
		        else{
		        	console.log('No TER')
		        }
			}
			else
			{
				console.log('Error desconocido',data)
			}
		}
	);
}

function showDropDown(e){
	cleanForm("#taskForm");
	$("#responsibleSelector option[value="+me+"]").attr("selected","selected")
	$("#accountableSelector option[value='']").attr("selected",true)
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

function showMoreFields(e){
	e.preventDefault();
  	e.stopPropagation();
	$(function(){
		if ($("#hiddenFields").hasClass('hide')) {
	  		$("#hiddenFields").removeClass('hide');
	  		$("#taskShowMoreIcon").removeClass('glyphicon-chevron-down')
	  		$("#taskShowMoreIcon").addClass('glyphicon-chevron-up')
		}	
		else{
			$("#hiddenFields").addClass('hide');
			$("#taskShowMoreIcon").removeClass('glyphicon-chevron-up')
	  		$("#taskShowMoreIcon").addClass('glyphicon-chevron-down')
		}
	});
}

$(document).on("submit","#taskForm", createTask)
$(document).on("focus","#miniNameTaskForm",hideDropDown)
$(document).on("submit","#miniTaskForm",miniCreateTask)
$(document).on("click",".set_task_done_btn", setTaskDone)
$(document).on("click",".set_task_assigned_btn", setTaskAssigned)
$(document).on("click",".delete_task_btn", deleteTask)
$(document).on("click",".edit_task_btn", editTask)
$(document).on("click",".one_task", showTask)
$(document).on("click","#taskAddBtn",showDropDown)
$(document).on("click","#cancelBtn", hideDropDown)
$(document).on("click","#taskShowMore",showMoreFields)
