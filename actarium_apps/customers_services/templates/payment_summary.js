var PaymentSummary = function(){

	// Data from Form
	this.number_of_members = 0
	this.number_of_months = 0
	this.payment_method = ""
	this.discount_code = ""

	//Calculated Data
	this.price_per_month = 0
	this.price_total_months = 0
	this.discount = 0
	this.total = 0
	// this.iva = 0
	// this.total_without_iva = 0


	function numberWithCommas(x) {
	    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
	}

	this.valuesForTemplate = function(){
		var values_with_comma = {
			"price_per_month": numberWithCommas(this.price_per_month),
			"number_of_members": numberWithCommas(this.number_of_members),
			"price_total_months": numberWithCommas(this.price_total_months),
			"discount": numberWithCommas(this.discount),
			"iva": numberWithCommas(this.total*0.16),
			"total": numberWithCommas(this.total),
			// "total_without_iva": numberWithCommas(this.total*0.84),
		}
		return values_with_comma
	}

	this.updateDiscount = function(){
		discount_code = this.discount_code;
		this_obj = this;
		sendNewAjax("{% url 'core:get_discount_value' %}",
			{"discount_code":discount_code},
			function(data){
				if (data.Error){
            		console.log(data.Error);
            		this_obj.discount = 0
            	}
            	else{
            		this_obj.discount = data.discount_value
            	}
            	this_obj.total = this_obj.price_total_months - this_obj.discount;
				
				this_obj.loadHtmlData();
				console.log(this_obj.valuesForTemplate())
			},
			{"method":"post"}
		)
	}



	this.updatePricePerMonth = function(){
		number_of_members = this.number_of_members
		this_obj = this;
		sendNewAjax(
			"{% url 'core:get_total_price' %}",
			{"quantity":number_of_members},
			function(data){
				if (data.Error){
					console.log("Ha ocurrido un error intentando recibir los datos del servidor por AJAX",data.Error)
				}
				else{
					this_obj.price_per_month = data.quantity
				}
				this_obj.price_total_months = this_obj.number_of_months*this_obj.price_per_month;
				console.log(this_obj)
				this_obj.updateDiscount();
			},
			{"method":"post"}
		)
	}

	
	this.loadHtmlData = function(){
		tpl = $("#paymentSummaryTpl").html()
		html_data = swig.render(tpl,{locals: this.valuesForTemplate() })
		$('#paymentSummaryTable').html(html_data);
	}

	this.updateWithForm = function(){
		number_of_members = $('#id_number_of_members').val();
		console.log(number_of_members)
		this.number_of_members = number_of_members;
		number_of_months =$('#id_number_of_months').val();
		console.log(number_of_months)
    	this.number_of_months = number_of_months;
    	this.payment_method = $('#id_payment_method').val();
    	this.discount_code = $('#id_discount').val()
    	// console.log(this.valuesForTemplate())
    }

    this.update = function(){
    	//get data from form
		this.updateWithForm();
		//update object data
		this.updatePricePerMonth();
	}
}

payment_summary_obj = new PaymentSummary();