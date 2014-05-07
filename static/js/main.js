// Avoid `console` errors in browsers that lack a console.
if (!(window.console && console.log)) {
    (function() {
        var noop = function() {};
        var methods = ['assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error', 'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log', 'markTimeline', 'profile', 'profileEnd', 'markTimeline', 'table', 'time', 'timeEnd', 'timeStamp', 'trace', 'warn'];
        var length = methods.length;
        var console = window.console = {};
        while (length--) {
            console[methods[length]] = noop;
        }
    }());
}

// Place any jQuery/helper plugins in here.
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

$(document).ready(function(){
    $("#log-sup").on("click", function(e){
        e.preventDefault();
        $("#username").focus();
    });

    //-------------------<letra blanca del perfil on hover>-------------------------//
    $(".dropdown-menu li.current-user").hover(
        function(e){
            $(".content-box *").addClass("color-fff");
        },
        function(e){
            $(".content-box *").removeClass("color-fff");
        }
    );
    //-------------------</letra blanca del perfil on hover>-------------------------//

    //------ <On Login Submit >--------------/
    $("#close-login-menu").on("click",function(e){
        e.preventDefault();
        $(".dropdown-menu").removeClass("disblock");
    });
    //------ </On Login Submit >--------------/

    //----------<On Menu hover>-------------------/
    $(".navbar-element").hover(function(){
            $(this).children("div.navbar-item").addClass("navbar-item-hover");
            $(this).children("div.navbar-button-propierties").css({"height":"15px"}, 100);
    },function(){
        if(!$(this).hasClass("menu-active")){
            $(this).children("div.navbar-item").removeClass("navbar-item-hover");
            $(this).children("div.navbar-button-propierties").css({"height":"10px"}, 100);
        }
    });
    //----------</On Menu hover>-------------------/

    //----------------<>-------------------/
    $("#drop-d-menu").on("click",function(){
        $("#navbar-button-container").slideToggle("fast");
    });
    //----------------</>-------------------/

    //----------------<feedback>-------------------/
    $("#feed-option, #callFeed, #menu-feed").on("click", openFeedBack);
    $("#close-feed, #cancel-feed").on("click", closeFeedBack);
    function openFeedBack(e){
        e.preventDefault();
        $("#feed-modal").modal().animate({
            'right':'0px'
        });
    }
    function closeFeedBack(e) {
        e.preventDefault();
        $("#feed-modal").animate({
            'right':'-505px'
        }).modal('hide');
    }
    var num = 0;
    $("#feed-imput > button.btn").on("click", function(){
        num = $(this).val();
        $("#textComent").focus();
        ph = "";
        switch(parseInt(num)){
            case 0 : ph = "Escribenos tus comentarios..."; break;
            case 1 : ph = "Tienes alguna idea para Actarium? Escribenos."; break;
            case 2 : ph = "Encontraste un error? Escribenos"; break;
            case 3 : ph = "Tienes una duda o una pregunta en general?"; break;
            default: ph = "Error";
        }
        $("#textComent").attr({"placeholder": ph});
    });
    function enablendButton(e) {
        if($("#textComent").val().length>0){
            $("#send-feed-back").removeClass("disabled");
        }
        else{
            $("#send-feed-back").addClass("disabled");
        }
    }
    $("#textComent").on("keyup",enablendButton);
    $("#send-feed-back").on("click",function(e){
        e.preventDefault();
        if(!$(this).hasClass("disabled")){
            comment = $("#textComent");
            mail = $("#fb-email");
            params = {"rate": num, "comment": comment.val(), "email": mail.val()}
            $("#send-feed-back").addClass("disabled");
            sendAjax("/feed-back",params, "#load-feed-back", function(data) {
                console.log(data)
                if(data['error']){
                    $("#send-feed-back").removeClass("disabled");
                    mail.focus().parent().addClass("error")
                }
                else{
                    setAlertMessage("Muchas gracias", "Tu mensaje ha sido enviado, te agradecemos por escribirnos y esperamos poder responderte pronto.")
                    comment.val("");
                    mail.parent().removeClass("error");
                    $("#feed-imput > button.btn").removeClass("active");
                    closeFeedBack(e);  
                }
            });//sendAjax
        }
    });
    //----------------</feedback>-------------------/

    //terms cheched
    $("#term_privacy").on("change", function(){
        if($(this).is(':checked')){
            $("#btn-submit").attr("disabled", false)
        } else {
            $("#btn-submit").attr("disabled", true)
        }
    });

});
function goToByScroll(element, callback){// Scroll
    $('html,body').animate({
        scrollTop: $(element).offset().top - 100},
        'slow', callback);
}


function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}

function setAlert(tittle, message, type){
    var l = message.length;
    var t=0;
    if (l===0) t=0;
    else if (l<=50)  t=3000;
    else if (l<=100) t=5000;
    else if (l<=200) t=6000;
    else if (l> 200) t=7000;
    $(type+" h4").html(tittle);
    $(type+" p").html(message);
    $(type).fadeIn().delay(t).fadeOut(1500);
}
function setAlertError(t, m){
    setAlert(t, m, '#alert-error');
}
function setAlertMessage(t, m){
    setAlert(t, m, '#alert-message');
}
function sendAjax(url, params, load_elem, myCallback){
    // $(load_elem).show().html('<img src="/static/img/load16.gif" />');
    $("#ac-load").fadeIn().html('<img src="/static/img/load.gif" />');
    $.get(url, params, function(data,error) {
            myCallback(data,error);
            // $(load_elem).hide();
            $("#ac-load").fadeOut();
        }
    );
}

function sendNewAjax(url, params, myCallback, args){
    if (typeof args === "undefined") {
        load_elem = "#ac-load";
    } else {
        load_elem = args.load_elem || "#ac-load";
    }
    $(load_elem).fadeIn().html('<img src="/static/img/load.gif" />');
    if (typeof args === "undefined" || args.method === "get") {
        $.get(url, params)
        .done(function(data) {
            myCallback(data);
            $(load_elem).fadeOut();
        })
        .fail(function(error){
            console.log(error);
        });
    } else if (args.method === "post") {
        $.post(url, params)
        .done(function(data) {
            myCallback(data);
            $(load_elem).fadeOut();
        })
        .fail(function(error) {
            console.log(error);
        });
    }
}
/*Dropdown Actarium*/
function restartMenus(){
    $(".second-menu").slideUp(200);
    $(".first-menu").slideDown(150);
}
$(".actarium-dropdown").on("click", function (e){
    e.preventDefault();
    var this_dropdown = $(this).parent().find(".dropdown-container");
    $(".dropdown-container").not(this_dropdown).hide();//hide every .dropdown-container except this_dropdown
    this_dropdown.slideToggle(100);
    restartMenus();
});
$(".close-popover").on("click", function (e){
    /*Close dropdown container*/
    e.preventDefault();
    e.stopPropagation();
    $(this).closest(".dropdown-container").hide();
    restartMenus();
});
$(".actarium-dropdown + .dropdown-container .open-second-menu").on("click", function (e) {
    e.preventDefault();
    console.log("hola")
    changeDropDownMenus($(this));
})
function changeDropDownMenus(elem){
    var second_menu = elem.closest(".dropdown-body").find(".second-menu");
    var first_menu = elem.closest(".dropdown-body").find(".first-menu");

    second_menu.slideDown(150);
    first_menu.slideUp(200, function(){$(".first-element").focus();});

    second_menu.find(".back").on("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        first_menu.slideDown(150);
        second_menu.slideUp(200);
    });
}
/*Close Dropdown Actarium*/

$("#language-form button").on("click", function (e){e.preventDefault();$("#language-selected").val($(this).attr("data-language"));$("#language-form").submit();})

// $(document).ready(main);
