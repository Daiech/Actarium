{% load i18n orgs_ttag gravatartag %}
invitationResult = function (data){//Resultados de la invitacion (agrega si TRUE, error si False)
    if(data['invited']){
    	li = "";
        users = [data.user];
        ctx = {members : users, watcher_is_org_admin: {{ is_org_admin|lower }}, watcher_id: {{ user.id }}}
        $("#orgListMembers").append(swig.render($("#orgListMembersTpl").html(), {locals: ctx}));
        setAlertMessage("{% trans 'Usuario agregado' %}", data.invited);
        //clean result
        $("#org-user-" + data.user.id).empty().fadeOut().remove();
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
    sendAjax("{% url 'set_invitation' %}",ctx, invitationResult, {"method": "post"});
    $("#search-result").fadeOut(300,function (argument) {
        $(this).empty().show().removeClass("user-li");;
    });
    $("#newmember").focus();
    $("#message-search").html(message);
}
function sendInvitationFromAdmin(e){
	e.preventDefault();
	var mail = $(this).attr("data-email");
    var uname = $(this).attr("data-username");
    sendNewAjax("{% url 'set_org_invitation' org.slug %}", {"mail": mail, "uname": uname}, invitationResult, {"method": "post"});
}
function appendToList (li) {
    $("#search-result").show().html(li);
    $("#org-user-list").hide();
}
function showMemberList(data){//Muestra la lista de posibles miembros a agregar
    p = "";
    if(data.new_user){//No es usuario de la base de datos
        if(data.new_user.email.length > MAX_LENGTH){p="...";}else{p="";}
        var view = {
            "mail":     data.new_user['email'],
            "gravatar": data.new_user['gravatar'],
            "username": data.new_user['username'],
            "p": p
        }
        appendToList(swig.render($("#new-user-template").html(), {locals: view}));
        $("#message-search").html("<strong>" + view.mail + "</strong> {% trans 'aún no disfruta de Actarium. Agrega sus datos y le enviaremos una invitación al correo electrónico.' %}")
    }
    else{//es usuario de la base de datos

        $("#message-search").html("{% trans 'Haz click en el nombre para invitar al grupo.' %}")
        li = "";
        users = [];
        for (var i = 0; i < data.users.length; i++) {
            // users.append({});
            user_to_invite = data.users[i]['full_name'];
            if(user_to_invite.length > MAX_LENGTH){p="...";}else{p="";}
            users[i] = {
                "id": data.users[i].id,
                "email": data.users[i].email,
                "username": data.users[i].username,
                "image": data.users[i].gravatar, 
                "get_full_name": user_to_invite,
                "full_name": user_to_invite.substring(0,MAX_LENGTH) + p,
                "is_member": data.users[i].is_member,
                "is_org_member": data.users[i].is_org_member
            }
        };
        appendToList(swig.render($("#org-user-template").html(), {locals: users}));
        
    }
}
function show_search_result(data){//lista los usuarios disponibles a invitar
    if(data){
    	if (data.forbbiden){
    		setAlertError("{% trans 'Error' %}", data.forbbiden);
    	}else{
            showMemberList(data);//Muestra la lista de posibles miembros a agregar
    	}
    }else{//error en el server
        setAlertError("{% trans 'Error en el servidor' %}", "{% trans 'Lo sentimos, algo salió mal en el servidor.Por favor recarga la página e intenta de nuevo' %}")
    }
}
function getSearch () {
	var user = $("#newmember").val();
    sendNewAjax("{% url 'get_users_list' org.slug  %}", {search: user}, show_search_result);
}
function searchMember(e){
	e.preventDefault();
    if(e.keyCode==13){
	    getSearch();
    }
}
$(document).on("click", "a.disabled", function (e) {
    e.preventDefault();
});
$(document).on("click", "a.event-org-inv", sendInvitationFromAdmin);
$(document).on("click", "#add-new-user", sendInvitationToNewUser);
$(document).ready(function() {
	MAX_LENGTH = 25;
	$(".user-list").niceScroll();
	$("#button-search").on("click", function (e) {
		e.preventDefault();
		getSearch();
		$("#newmember").focus();
	});	
	$("#newmember").on("keyup", searchMember);
	$(".actarium-dropdown").on("click", function (e) {
		$("#newmember").attr("autofocus","autofocus")
		setTimeout(function(){$("#newmember").focus();}, 1);
	});
});