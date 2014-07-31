{% load i18n orgs_ttag gravatartag %}
$(document).ready(function() {
	MAX_LENGTH = 60;
	message = "{% trans 'Escribe el nombre de usuario o correo electr&oacute;nico del nuevo miembro del grupo.' %}";
	$("#message-search").html(message);
	$(".user-list").niceScroll();
	$("#button-search").on("click", function (e) {
		e.preventDefault();
		getSearch();
		$("#newmember").focus();
	});
	$("#newmember").on("keyup", searchMember);//INVITACIONES MAIN 
	$("#add-member").on('click focus', function(){//dar FOCO al input para buscar miembros
	    $("#add-member-menu").addClass("disblock");
	    $("#newmember").focus();//give the focus to the input to search members
	});
	$("#close-add-member").on("click",function(e){//boton cerrar dropdown
	    $("#add-member-menu").removeClass("disblock");//Close the dropdown menu to add members
	});
	$(".actarium-dropdown").on("click", function (e) {
		$("#newmember").attr("autofocus","autofocus")
		setTimeout(function(){$("#newmember").focus();}, 1);
	})
	showIconCloseOnHover();
	load_org_member_list();
});
function load_org_member_list () {
	users = {};
	{% for u in group.organization.get_members %}{% is_member_of_group "u" "group" as is_member %}
	users[{{ forloop.counter0 }}] = {"id": "{{ u.id }}","email": "{{ u.email }}","username": "{{ u.username }}","image": "{{ u.email|showgravatar:28 }}","full_name": "{{ u.get_full_name|truncatechars:24 }}", "is_member": {{ is_member|lower }}};{% endfor %}
	$("#org-user-list").html(swig.render($("#org-user-template").html(), {locals: users}));
}
function append_org_member(u){
	users = {};
	users[0] = {"id": u.iid,"email": u.email, "username": u.username, "image": u['gravatar'],"full_name": u['full_name'], "is_member": true};
	$("#org-user-list").append(swig.render($("#org-user-template").html(), {locals: users}));
}
function showIconCloseOnHover(){
    $(".list-member-item").hover(function(){  
        $(this).find("i.icon-remove").show(10)  
    },function(){                      
        $(this).find("i.icon-remove").hide(30)
    })
}
invitationResult = function (data, append_to_org_list){//Resultados de la invitacion (agrega si TRUE, error si False)
    if(data['invited']){    //USUARIO INVITADO
    	var is_admin = "{{is_admin}}";
    	var user = {
			id: data['iid'], is_active: data['is_active'],
			username: data['username'], first_name: data['first_name'], last_name: data['last_name'],
			get_full_name: data['full_name'], email: data['email'], gravatar: data['gravatar'],
			roles: {is_member: true,is_secretary: false,is_admin: false}
		}
    	var team_members = team.members;
    	team.members = [user]; 
		$("#teamList").append(swig.render($("#teamListTpl").html(),{locals: team}));
		team.members = team_members;
		team.members.push(user);
		setAlertMessage("{% trans 'Invitado' %}", data['message'])
        showIconCloseOnHover()
		$("td input[type='checkbox']").on("click", setRole);
        $("#newmember").val("");
        if (!append_to_org_list){append_org_member(data);}
    }else{//EL USUARIO YA ESTA INVITADO
        if(data["message"]){
            setAlertError("{% trans 'Informaci&oacute;n' %}","("+data['email']+") "+data['message'])
        }
        else{
            //si no hay mensaje, error desconocido
            if(data["error"]){
            	setAlertError("{% trans 'Ups! Algo sali&oacute; mal :(' %}",data['error'])
            }
            else{
            	setAlertError("{% trans 'Ups! Algo sali&oacute; mal :(' %}","{% trans 'Por favor recarga la p&aacute;gina e intenta de nuevo' %}")
            }
        }
    }
}
sendInvitation = function (elem, callback) {
	var mail = elem.attr("data-email");
    var uname = elem.attr("data-username");
    var group_id = $("#group_id").val();
    sendNewAjax("{% url 'set_invitation' %}", {"pk":group_id, "mail": mail}, callback);
}
function showIconAddMemberOnHover(){
    // mostrar flecha sobre usuario
    $(".user-li").hover(
        function(){
            $(this).find("i").toggleClass("hidden");
    })
}
function sendInvitationToNewUser(e){
	e.preventDefault();
	var ctx = {
		"new": 1,
		"pk": $("#group_id").val(),
		"mail": $("#new-user-email").val(),
		"uname": $("#new-user-uname").val(),
		"firstname": $("#new-user-firstname").val(),
		"lastname": $("#new-user-lastname").val(),
		}
	sendAjax("{% url 'set_invitation' %}",ctx,"",invitationResult);
	$("#search-result").fadeOut(300,function (argument) {
		$(this).empty().show().removeClass("user-li");;
	});
    $("#newmember").focus();
    $("#message-search").html(message);
}

function appendMemberToList(data){//Muestra la lista de posibles miembros a agregar
	if(data.mail_is_valid){
        if(data.new_user){//No es usuario de la base de datos
        	if(data['mail'].length > MAX_LENGTH)
                p="..."
            var view = {
            	"mail": data['mail'],
            	"gravatar": data['gravatar'],
            	"username": data['username'],
            	"p": p
            }
            $("#search-result").html(swig.render($("#new-user-template").html(), {locals:view}));
            $("#message-search").html("<strong>" + view.mail + "</strong> a&uacute;n no disfruta de Actarium. Agrega sus datos y le enviaremos una invitaci&oacute;n al correo electr&oacute;nico.")
            $("#add-new-user").on("click", sendInvitationToNewUser);
        }
        else{//es usuario de la base de datos

            $("#message-search").html("<strong>" + data.username + "</strong> {% trans 'hace parte de Actarium, haz click en el nombre para invitar.' %}");
        	
            user_to_invite = data['mail']+" ("+data['username']+")";
            if(user_to_invite.length > MAX_LENGTH)
                p="..."
            $("#search-result").html(
                "<li class='user-li'>"+
                "<a href='#invite-user' data-email='"+data['mail']+"' data-username='"+data['username']+"' >"+
                "<img class='img30' src='"+data['gravatar']+"' alt='"+data['username']+"' />"+
                user_to_invite.substring(0,MAX_LENGTH)+p+
                '<i class="icon-accept pull-right icon-ok icon-white hidden"></i>'+
                "</a>"+
                "</li>"
                );
            
        }
        showIconAddMemberOnHover()//muestra icono "onHover" de la lista de miembros buscados
    }
}
function sendInvitationOnClick(e){//escucha el evento click para agregar al usuario al grupo
    e.preventDefault();
    sendInvitation($(this), invitationResult);
    $(this).parent().fadeOut(300, function (e){
    	$(this).empty().show().removeClass("user-li");
    });
    $("#newmember").focus();
    $("#message-search").html(message);
}
$(document).on("click", ".user-li > a", sendInvitationOnClick);

function show_search_result(data){//lista los usuarios disponibles a invitar
    if(data){
    	if (data.forbbiden){
    		setAlertError("{% trans 'Error' %}", data.forbbiden);
    	}else{
            p="";
            if(data.users){//el email valido, viene una lista de usuarios existentes
                appendMemberToList(data);//Muestra la lista de posibles miembros a agregar
            }
            else{//el correo es invalido o no hay resultados de usuarios existentes
            	$("#message-search").html("{% trans 'Asegurate de escribir correctamente el correo electr&oacute;nico.' %}");
                // org-user-template
                $("#search-result").html("<li style='list-style:none'>"+
                                            "<a href='#'>"+("No hay resultados").substring(0,MAX_LENGTH)+
                                            "</a>"+
                                        "</li>")
            }
    	}
    }else{//error en el server
        setAlertError("{% trans 'Error en el servidor' %}", "{% trans 'Lo sentimos, algo salió mal en el servidor.Por favor recarga la página e intenta de nuevo' %}")
    }
}
function getSearch () {
	var user = $("#newmember").val();
    sendNewAjax("{% url 'get_users_list' group.organization.slug  %}", {search: user}, show_search_result);
}