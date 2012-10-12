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
        function(e){$(".content-box *").addClass("color-fff")},
        function(e){$(".content-box *").removeClass("color-fff")}
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

$(document).on("ready",main);
