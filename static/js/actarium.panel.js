/**
 * Actarium Panel
 * Crea paneles dentro del Procesador de actas
 *
 * Requires:
 *  jQuery
 *  Swig
 *
 * Develop by Mauricio Aizaga. @MaoAiz to Daiech
 */

$(document).on("click", ".close-panel", closePanel);
function loadPanelContent(html_content){
	$("#activity-content").html(html_content);
}
function loadPanel (a, callback) {
	ctx = a;
	$("#minutesPanel").html(swig.render($("#minutesPanelTpl").html(), {locals: ctx})).removeClass("hidden");
	$(".btn-pull-right").addClass("btn-pull-right-with-panel");
	$("#activity").removeClass("hidden");
	$("#minutes-processor-container").addClass("mpc");
	$(".popover-element").popover({trigger: 'hover'});
	$("#activity-content").html("loading...");
	callback();
}
function closePanel (e) {
	e.preventDefault();
	$("#minutesPanel").addClass("hidden");
	$("#activity").addClass("hidden");
	$("#minutes-processor-container").removeClass("mpc");
	$(".btn-pull-right").removeClass("btn-pull-right-with-panel");
}