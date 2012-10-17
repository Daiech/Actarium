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
    
    $("#add-member").on('click focus', function(e) {
        $(this).next(".dropdown-menu").addClass("disblock")
        $("#newmember").focus()
    });

    $("#close-add-member").on("click",function(e){
        $(this).parent().parent().removeClass("disblock")
    });
    $("#newmember").on("keyup",function(e){
        if(e.keyCode==13){
            var user=$("#newmember").val()
            //go to the server:users
            
                $("#search-result").html("<li><a href='#' class='btn btn-link'>"+user+"</a></li>")          
            setAlert("Enviado","La invitación a unirse al grupo ha sido enviada a "+ user)
            $(this).val("")

            }
    })

}

function setAlert(tittle, message){
    $("#alert-message h4").text(tittle)
    $("#alert-message p").text(message)
    $("#alert-message").fadeIn().delay(5000).fadeOut(1500)
    
}

$(document).on("ready",main);
