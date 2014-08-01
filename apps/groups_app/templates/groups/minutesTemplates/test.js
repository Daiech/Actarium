function sendForm(e){
	e.preventDefault();
	e.stopPropagation();
 	console.log($(this).serialize())
}

function submitForm(){
	$("#form-new-minutes").submit()
}


$(document).on("submit","#form-new-minutes", sendForm)
$(document).on("click","#sendForm", submitForm)


function readForm(){$.each(serialized.split('&'), function (index, elem) {
   var vals = elem.split('=');
   $("[name='" + vals[0] + "']").val(vals[1]);
});}

tinyMCE.triggerSave();