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
			"total": numberWithCommas(this.total,
		}
		return values_with_comma
	}

	this.updatePricePerMonth = function(){
		number_of_members = this.number_of_members
		sendNewAjax(
			"{% url 'core:get_total_price' %}",
			{"quantity":number_of_members},
			function(data){
				if (data.Error){
					console.log("Ha ocurrido un error intentando recibir los datos del servidor por AJAX")
				}
				else{
					this.price_per_month = data.quantity
				}
			},
			{"method":"post"}
		)
	}

	this.updateDiscount = function(){
		discount_code = this.discount_code;
		sendNewAjax("{% url 'core:get_discount_value' %}",
			{"discount_code":discount_code},
			function(){
				if (data.Error){
            		console.log(data.Error)
            	}
            	else{
            		$('#discountValue').html(numberWithCommas(data.discount_value))
            		setTotalPrice();
            	}
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
		this.number_of_members = $('#id_number_of_members').val();
    	this.number_of_months = $('#id_number_of_months').val();
    	this.payment_method = $('#id_payment_method').val();
    	this.discount_code = $('#id_discount').val()
    }

    this.update = function(){
    	//get data from form
		this.updateWithForm();
		//update object data
		this.updatePricePerMonth();
		this.price_total_months = this.number_of_months*this.price_per_month;
		this.updateDiscount();
		this.total = this.price_total_months - this.discount
		//update html
		this.loadHtmlData()
	}
}

payment_summary_obj = new PaymentSummary();