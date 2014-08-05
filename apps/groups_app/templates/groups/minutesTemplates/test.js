function sendForm(e){
	e.preventDefault();
	e.stopPropagation();
	tinyMCE.triggerSave();
	$.each($("#minutes textarea"),function(index,value){$(this).val($(this).val().replace(/\ /g, '&nbsp;'))});
 	console.log($(this).serialize())
}

function submitForm(){
	$("#form-new-minutes").submit()
}


setForm = function(){
   serialized = $("#form-new-minutes").serialize();
   $.each(serialized.split('&'), function (index, elem) {
	   var vals = elem.split('=');
	   $("[name='" + vals[0] + "']").val(vals[1]);
	});
   $.each($("#minutes textarea"),function(index,value){console.log(index);tinyMCE.activeEditor.setContent(tinyMCE.DOM.decode(unescape($(value).val())))});
}


$(document).on("submit","#form-new-minutes", sendForm)
$(document).on("click","#sendForm", submitForm)


