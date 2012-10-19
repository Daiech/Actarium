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

function main(){
    //-------------------<letra blanca del perfil on hover>-------------------------//
    $("ul.dropdown-menu li.current-user").hover(
    function(e){
        $(".content-box *").addClass("color-fff")
    },
    function(e){
        $(".content-box *").removeClass("color-fff")
    }
);
    //-------------------</letra blanca del perfil on hover>-------------------------//
    
    //------<No cierra el Menú de login al dar click>---------------/
    $(".next-li").focus(function(e){
        $("ul.dropdown-menu").addClass("disblock")
    }).blur(function(e){
        // $("ul.dropdown-menu").removeClass("disblock")
    });
    //------ </No cierra el Menú de login al dar click>--------------/

    //------ <On Login Submit >--------------/
    $("#close-login-menu").on("click",function(e){
        e.preventDefault();
        $("ul.dropdown-menu").removeClass("disblock");
    });
    //------ </On Login Submit >--------------/
}

function setAlert(tittle, message){
    var l = message.length;
    var t=0;
    if (l===0) t=0;
    else if (l<=50)  t=2000;
    else if (l<=100) t=3000;
    else if (l<=200) t=5000;
    else if (l> 200) t=7000;
    $("#alert-message h4").text(tittle);
    $("#alert-message p").text(message);
    $("#alert-message").fadeIn().delay(t).fadeOut(1500);
    
}

function sendAjax(url,data,destiny){
    $.get(url, data, function(data) {
            $(""+destiny).text(data);
        }
    );
}

$(document).on("ready",main);
