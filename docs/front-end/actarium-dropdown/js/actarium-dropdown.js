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