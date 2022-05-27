 function click_ahref (){

    document.getElementById("forprint").style="display: block";
    document.getElementById("save_data").style="display: block";
    document.getElementById("button_save").style="display: none";

    //class
    $('.currency_view').text(document.getElementById("currency").value);
    $('.product_view').text(document.getElementById("name_product").value);
    $('.period_view').text(document.getElementById("value_days").value);

    var quantity_valid = (document.getElementById("value_all").value).split(",").join(".");
    var days_valid = (document.getElementById("value_days").value).split(",").join(".");
    var price_valid = (document.getElementById("price_product").value).split(",").join(".");


	/*Нормируемые затраты---------------------------------------------------*/
    /* Check for input with a specific attribute */

    if($('.sumItg').is('input[data-type=inp]')){
      document.getElementById("name_td_norm").style="display: block";
      document.getElementById("name_td_norm_estimate").style="display: block";
    }else{
      document.getElementById("name_td_norm").style="display: none";
      document.getElementById("name_td_norm_estimate").style="display: none";
    };

	var sumItg = 0;
	var input = document.querySelectorAll("[data-type=inp]");
	var i = input.length;

    var count = 0;

    var th_mas = new Array();
    var val_mas = new Array();
    var val_mas_estimate= new Array();
    var price_mas = new Array();
    var cost_mas = new Array();
    var cost_mas_estimate = new Array();

    var table = new Array();

    var r_table="";

    var table_estimate = new Array();
    var r_table_estimate="";

	while(i--) {
		if(input[i].className == 'sumItg') {

            var th = input[i].value = input[i].value.split(",").join(".");
            var val = input[i].nextElementSibling.value = input[i].nextElementSibling.value.split(",").join(".");;
            var price = input[i].nextElementSibling.nextElementSibling.value = input[i].nextElementSibling.nextElementSibling.value.split(",").join(".");

            var cost = val * price;
            var cost_estimate = cost * quantity_valid;

			sumItg += cost;

            th_mas[i]= th;
            val_mas[i]= val;
            val_mas_estimate[i]= val * quantity_valid;
            price_mas[i]= price;
            cost_mas[i]= cost.toFixed(2);
            cost_mas_estimate[i]= cost_estimate.toFixed(2);

            table[count]= "<tr><td>" + th_mas[i] + "</td><td>" + val_mas[i] + "</td><td>" + price_mas[i] + "</td><td>" + cost_mas[i] + "</td></tr>";
            table_estimate[count]= "<tr><td>" + th_mas[i] + "</td><td>" + val_mas_estimate[i] + "</td><td>" + price_mas[i] + "</td><td>" + cost_mas_estimate[i] + "</td></tr>";

            count = count + 1;
		}
    }




	for (i = 0; i < table.length; i++) {
		r_table +=table[table.length-1/1-i/1];
		}
		document.getElementById('td_norm').innerHTML = r_table;

		var sumItg_norm = sumItg;

	for (i = 0; i < table_estimate.length; i++) {
		r_table_estimate +=table_estimate[table_estimate.length-1/1-i/1];
		}

		document.getElementById('td_norm_estimate').innerHTML = r_table_estimate;

	/*Трудозатраты затраты-------------------------------------------------------*/

		/* Check for input with a specific attribute */

		if($('.sumItg').is('input[data-type=work]')){
		  document.getElementById("name_td_work").style="display: block";
		  document.getElementById("name_td_work_estimate").style="display: block";
		}else{
		  document.getElementById("name_td_work").style="display: none";
		  document.getElementById("name_td_work_estimate").style="display: none";
		};

		var sumItg = 0;
		var input = document.querySelectorAll("[data-type=work]");
		var i = input.length;

		var count = 0;

		var th_mas = new Array();
		var val_mas = new Array();
		var zp_mas = new Array();
		var percent_zp_mas = new Array();

		var cost_mas = new Array();
		var cost_estimate_mas = new Array();

		var table_work = new Array();
		var r_table_work="";

		var table_work_estimate = new Array();
		var r_table_work_estimate="";
		
		var price_cost = new Array();


		while(i--) {

			if(input[i].className == 'sumItg') {

				var th = input[i].value = input[i].value.split(",").join(".");
				var val = input[i].nextElementSibling.value = input[i].nextElementSibling.value.split(",").join(".");;
				var zp = input[i].nextElementSibling.nextElementSibling.value = input[i].nextElementSibling.nextElementSibling.value.split(",").join(".");

				var percent_zp = input[i].nextElementSibling.nextElementSibling.nextElementSibling.value = input[i].nextElementSibling.nextElementSibling.nextElementSibling.value.split(",").join(".");

				var equal = val * (zp/30) * days_valid;

				percent_zp = (percent_zp.split("%").join(""))/100;

				var deductions = equal * percent_zp;

				sumItg += equal*100/100 + deductions*100/100;


				th_mas[i]= th;
				val_mas[i]= val;
				zp_mas[i]= zp;
				percent_zp_mas[i]= percent_zp;

				cost_mas[i] = (val_mas[i]*((zp_mas[i]*(1+percent_zp_mas[i]))/30)*days_valid)/quantity_valid;

				cost_estimate_mas[i] = (val_mas[i]*((zp_mas[i]*(1+percent_zp_mas[i]))/30)*days_valid);


				cost_mas[i] = cost_mas[i].toFixed(2);

				cost_estimate_mas[i] = cost_estimate_mas[i].toFixed(2);
				
				
				price_cost[i] = cost_mas[i]/val_mas[i];
				price_cost[i] = price_cost[i].toFixed(2)

				table_work[count]= "<tr><td>" + th_mas[i] + "</td><td>" + val_mas[i] + " (чел.)</td><td>" + price_cost[i] + " (з/п с отч. - " + (percent_zp_mas[i]*100).toFixed(2) + "%)</td><td>" + cost_mas[i] + "</td></tr>";

				table_work_estimate[count]= "<tr><td>" + th_mas[i] + "</td><td>" + val_mas[i] + " (чел.)</td><td>" + (zp_mas[i]*(1+percent_zp_mas[i])).toFixed(2) + " (ср.мес з/п с отч. - " + (percent_zp_mas[i]*100).toFixed(2) + " %)</td><td>" + cost_estimate_mas[i] + "</td></tr>";

				count = count + 1;
			}
		}


		for (i = 0; i < table_work.length; i++) {
		r_table_work +=table_work[table_work.length-1/1-i/1];
		}

		document.getElementById('td_work').innerHTML = r_table_work;

		var sumItg_work = sumItg;

		for (i = 0; i < table_work_estimate.length; i++) {
		r_table_work_estimate +=table_work_estimate[table_work_estimate.length-1/1-i/1];
		}

		document.getElementById('td_work_estimate').innerHTML = r_table_work_estimate;

	/*Амортизационные затраты----------------------------------------------------*/

		/* Check for input with a specific attribute */

		if($('.sumItg').is('input[data-type=amort]')){
		  document.getElementById("name_td_amort").style="display: block";
		  document.getElementById("name_td_amort_estimate").style="display: block";
		}else{
		  document.getElementById("name_td_amort").style="display: none";
		  document.getElementById("name_td_amort_estimate").style="display: none";
		};

		var sumItg = 0;
		var input = document.querySelectorAll("[data-type=amort]");
		var i = input.length;

		var count = 0;

		var th_mas = new Array();
		var val_mas = new Array();
		var price_mas = new Array();
		var time_amort_mas = new Array();

		var cost_mas = new Array();
		var cost_mas_estimate = new Array();

		var table_amort = new Array();
		var r_table_amort="";

		var table_amort_estimate = new Array();
		var r_table_amort_estimate="";

		while(i--) {

			if(input[i].className == 'sumItg') {

				var th = input[i].value = input[i].value.split(",").join(".");
				var val = input[i].nextElementSibling.value = input[i].nextElementSibling.value.split(",").join(".");;
				var price = input[i].nextElementSibling.nextElementSibling.value = input[i].nextElementSibling.nextElementSibling.value.split(",").join(".");

				var time_amort = input[i].nextElementSibling.nextElementSibling.nextElementSibling.value = input[i].nextElementSibling.nextElementSibling.nextElementSibling.value.split(",").join(".");

				var equal = val * price;

				var deductions = equal * ((100/time_amort/100)*days_valid)/365;

				sumItg += deductions*100/100;


				th_mas[i]= th;
				val_mas[i]= val;
				price_mas[i]= price;
				time_amort_mas[i]= ((100/time_amort/100)*days_valid)/365;

				cost_mas[i] = (val_mas[i] * price_mas[i] * time_amort_mas[i])/quantity_valid;

				cost_mas_estimate[i] = (val_mas[i] * price_mas[i] * time_amort_mas[i]);

				cost_mas[i] = cost_mas[i].toFixed(2);

				cost_mas_estimate[i] = cost_mas_estimate[i].toFixed(2);

				table_amort[count]= "<tr><td>" + th_mas[i] + "</td><td>" + val_mas[i] + " (шт.)</td><td>" +  price_mas[i] + " (норма аморт. в год - " + (100/time_amort).toFixed(2) + " %)" + "</td><td>" + cost_mas[i] + "</td></tr>";

				table_amort_estimate[count]= "<tr><td>" + th_mas[i] + "</td><td>" + val_mas[i] + " (шт.)</td><td>" + price_mas[i] + " (норма аморт. в год - " + (100/time_amort).toFixed(2) + " %)" + "</td><td>" + cost_mas_estimate[i] + "</td></tr>";

				count = count + 1;
			}
		}

		for (i = 0; i < table_amort.length; i++) {
		r_table_amort +=table_amort[table_amort.length-1/1-i/1];
		}

		document.getElementById('td_amort').innerHTML = r_table_amort;

		var sumItg_amort = sumItg;

		for (i = 0; i < table_amort_estimate.length; i++) {
		r_table_amort_estimate +=table_amort_estimate[table_amort_estimate.length-1/1-i/1];
		}

		document.getElementById('td_amort_estimate').innerHTML = r_table_amort_estimate;

	/*Накладные затраты-------------------------------------------------------------------*/

		/* Check for input with a specific attribute */

		if($('.sumItg').is('input[data-type=other]')){
		  document.getElementById("name_td_other").style="display: block";
		  document.getElementById("name_td_other_estimate").style="display: block";
		}else{
		  document.getElementById("name_td_other").style="display: none";
		  document.getElementById("name_td_other_estimate").style="display: none";
		};

		var sumItg = 0;
		var input = document.querySelectorAll("[data-type=other]");
		var i = input.length;

		var count = 0;

		var th_mas = new Array();
		var val_mas = new Array();
		var price_mas = new Array();
		var cost_mas = new Array();

		var table_other = new Array();

		var r_table_other="";

		var table_other_estimate = new Array();
		var r_table_other_estimate="";

		while(i--) {

			if(input[i].className == 'sumItg') {

				var th = input[i].value = input[i].value.split(",").join(".");
				var val = input[i].nextElementSibling.value = input[i].nextElementSibling.value.split(",").join(".");;
				var price = input[i].nextElementSibling.nextElementSibling.value = input[i].nextElementSibling.nextElementSibling.value.split(",").join(".");

				var cost = val * price;

				sumItg += cost;

				th_mas[i]= th;
				val_mas[i]= val;
				price_mas[i]= price;
				cost_mas[i]= cost/quantity_valid;

				table_other[count]= "<tr><td>" + th_mas[i] + "</td><td>" + val_mas[i] + "</td><td>" + price_mas[i] + "</td><td>" + cost_mas[i].toFixed(2) + "</td></tr>";
				table_other_estimate[count]= "<tr><td>" + th_mas[i] + "</td><td>" + val_mas[i] + "</td><td>" + price_mas[i] + "</td><td>" + cost.toFixed(2) + "</td></tr>";

				count = count + 1;
			}
		}

	for (i = 0; i < table_other.length; i++) {
		r_table_other +=table_other[table_other.length-1/1-i/1];
		}

		document.getElementById('td_other').innerHTML = r_table_other;

		var sumItg_other = sumItg;


	for (i = 0; i < table_other_estimate.length; i++) {
		r_table_other_estimate +=table_other_estimate[table_other_estimate.length-1/1-i/1];
		}

		document.getElementById('td_other_estimate').innerHTML = r_table_other_estimate;

		/*Исходники-------------------------------------------------------------*/

		document.getElementById('source_period').innerHTML = days_valid;
		document.getElementById('source_all').innerHTML = quantity_valid;
		document.getElementById('source_price').innerHTML = price_valid;

		/*Рентабельность расчёт--------------------------------------------------*/

		document.getElementById('r_goods').innerHTML = (((price_valid*100/100 - (sumItg_norm + (sumItg_work + sumItg_amort + sumItg_other)/quantity_valid))/price_valid*100/100)*100).toFixed(2);

		document.getElementById('parent').innerHTML = (sumItg_norm + (sumItg_work + sumItg_amort + sumItg_other)/quantity_valid).toFixed(2);

		document.getElementById('parent_estimate').innerHTML = (sumItg_norm * quantity_valid + (sumItg_work + sumItg_amort + sumItg_other)).toFixed(2);

		document.getElementById('variable_costs').innerHTML = sumItg_norm.toFixed(2);
		document.getElementById('fixed_costs').innerHTML = ((sumItg_work + sumItg_amort + sumItg_other)/quantity_valid).toFixed(2);

		document.getElementById('share_variable').innerHTML = (document.getElementById('variable_costs').innerHTML/document.getElementById('parent').innerHTML).toFixed(2);
		document.getElementById('share_fixed').innerHTML = (document.getElementById('fixed_costs').innerHTML/document.getElementById('parent').innerHTML).toFixed(2);

		document.getElementById('break_even').innerHTML = ((sumItg_work + sumItg_amort + sumItg_other)/(price_valid*100/100 - sumItg_norm*100/100)).toFixed(2);

        /*Django data----------------------------*/
        document.getElementById('cost_price').value = (sumItg_norm + (sumItg_work + sumItg_amort + sumItg_other)/quantity_valid).toFixed(2);


		var gorizont = new Array();
		var revenue = new Array();
		var cost = new Array();
		var constant_cost = new Array();

		var all_calc = document.getElementById('break_even').innerHTML * 2;
		var step_calc = all_calc/10;

		var counter = 0;

		var j = 0;
		var z_revenue =0;
		var z_cost = 0;

		while (counter < 10)
		{

		  gorizont[counter] = j.toFixed(2);
		  revenue[counter] = z_revenue.toFixed(2);
		  cost[counter] = z_cost + document.getElementById('fixed_costs').innerHTML * quantity_valid;
		  constant_cost[counter] = document.getElementById('fixed_costs').innerHTML * quantity_valid;


		  counter = counter + 1;
		  j = j + step_calc;
		  z_revenue = j * price_valid;
		  z_cost = j * document.getElementById('variable_costs').innerHTML;

		}

	var speedCanvas = document.getElementById("speedChart");

	Chart.defaults.global.defaultFontFamily = "Lato";
	Chart.defaults.global.defaultFontSize = 18;

	var dataFirst = {
		label: "Суммарные затраты",
		data: cost,
		lineTension: 0,
		fill: false,
		borderColor: 'red'
	  };

	var dataSecond = {
		label: "Постоянные затраты",
		data: constant_cost,
		lineTension: 0,
		fill: false,
	  borderColor: 'blue'
	  };

	var dataSecond_ = {
		label: "Выручка",
		data: revenue,
		lineTension: 0,
		fill: false,
	  borderColor: 'green'
	  };


	var speedData = {
	  labels: gorizont,
	  datasets: [dataFirst, dataSecond, dataSecond_]
	};

	var chartOptions = {
	  legend: {
		display: true,
		position: 'top',
		labels: {
		  boxWidth: 80,
		  fontColor: 'black'
		}
	  }
	};

	var lineChart = new Chart(speedCanvas, {
	  type: 'line',
	  data: speedData,
	  options: chartOptions
	});
}



/*Удаление родительского блока  - Удалить кнопка-----------------------------*/
$(document).on("click", ".del", function() {
       $(this).parent().remove();
});

		function added_norm() {

            var i = parseInt(document.getElementById('count_inp').value) + 1;
            document.getElementById('count_inp').value = parseInt(document.getElementById('count_inp').value) + 3;

            if(document.getElementById('materials').value !== ''){
                document.getElementById('materials').value = document.getElementById('materials').value + ' ' + i;
            }
            else{
                document.getElementById('materials').value = document.getElementById('materials').value + i;
            }

			$("<div class='param'><input autocomplete='off' required type='text' name='material_name["+ i +"]' placeholder='Наименование сырья' data-type='inp' class='sumItg' onblur='func(this.id,this.value)' value='' id='n_"+ i +"'> " +
				"<input autocomplete='off' min='1' required type='number' name='count["+ i +"]' placeholder='Расход на ед. продукции (число)' data-type='inp' onblur='func(this.id,this.value)' value='' id='n_"+ (i+1) +"'>" +
				" <input autocomplete='off' min='1' required type='number' name='cost["+ i +"]' placeholder='Цена сырья (число)' class='test' data-type='inp' onblur='func(this.id,this.value)' value='' id='n_"+ (i+2) +"'><span class='del'>&times;</span></div> " ).insertBefore("#form_status_added");

            document.getElementById("forprint").style="display: none";
            document.getElementById("save_data").style="display: none";
            document.getElementById("button_save").style="display: none";
		};


		function added_work() {

            var i = parseInt(document.getElementById('count_inp').value) + 1;
            document.getElementById('count_inp').value = parseInt(document.getElementById('count_inp').value) + 4;

            if(document.getElementById('labors').value !== ''){
                document.getElementById('labors').value = document.getElementById('labors').value + ' ' + i;
            }
            else{
                document.getElementById('labors').value = document.getElementById('labors').value + i;
            }

			$("<div class='param'><input autocomplete='off' required type='text' name='profession["+ i +"]' placeholder='Профессия' data-type='work' class='sumItg' onblur='func(this.id,this.value)' value='' id='n_"+ i +"'> " +
				"<input autocomplete='off' min='1' required type='number' name='number_of_people["+ i +"]' placeholder='Количество человек (число)' data-type='work' onblur='func(this.id,this.value)' value='' id='n_"+ (i+1) +"'> " +
				"<input autocomplete='off' min='1' required type='number' name='salary["+ i +"]' placeholder='Ср.месячная з/п (число)' class='test' data-type='work' onblur='func(this.id,this.value)' value='' id='n_"+ (i+2) +"'>" +
				" <input autocomplete='off' min='0' required type='number' name='deduction["+ i +"]' placeholder='% отч. от з/п в фонды (число)' onblur='func(this.id,this.value)' value='' id='n_"+ (i+3) +"'> <span class='del'>&times;</span></div> " ).insertBefore("#form_status_added_work");

            document.getElementById("forprint").style="display: none";
            document.getElementById("save_data").style="display: none";
            document.getElementById("button_save").style="display: none";

		};


		function added_amortization() {

            var i = parseInt(document.getElementById('count_inp').value) + 1;
            document.getElementById('count_inp').value = parseInt(document.getElementById('count_inp').value) + 4;

            if(document.getElementById('amortizations').value !== ''){
                document.getElementById('amortizations').value = document.getElementById('amortizations').value + ' ' + i;
            }
            else{
                document.getElementById('amortizations').value = document.getElementById('amortizations').value + i;
            }

			$("<div class='param'><input autocomplete='off' required type='text' name='equipment_name["+ i +"]' placeholder='Наименование оборудования' data-type='amort' class='sumItg' onblur='func(this.id,this.value)' value='' id='n_"+ i +"'> " +
				"<input autocomplete='off' min='1' required type='number' name='count_equipment["+ i +"]' placeholder='Количество ед. (число)' data-type='amort' onblur='func(this.id,this.value)' value='' id='n_"+ (i+1) +"'> " +
				"<input autocomplete='off' min='1' required type='number' name='cost["+ i +"]' placeholder='Цена за ед. (число)' class='test' data-type='amort' onblur='func(this.id,this.value)' value='' id='n_"+ (i+2) +"'> " +
				"<input autocomplete='off' min='1' required type='number' name='service_life["+ i +"]' placeholder='Срок службы - лет (число)' onblur='func(this.id,this.value)' value='' id='n_"+ (i+3) +"'> <span class='del'>&times;</span></div> " ).insertBefore("#form_status_added_amortization");

            document.getElementById("forprint").style="display: none";
            document.getElementById("save_data").style="display: none";
            document.getElementById("button_save").style="display: none";
		};


		function added_other() {

            var i = parseInt(document.getElementById('count_inp').value) + 1;
            document.getElementById('count_inp').value = parseInt(document.getElementById('count_inp').value) + 3;

            if(document.getElementById('invoices').value !== ''){
                document.getElementById('invoices').value = document.getElementById('invoices').value + ' ' + i;
            }
            else{
                document.getElementById('invoices').value = document.getElementById('invoices').value + i;
            }

			$("<div class='param'><input autocomplete='off' required type='text' name='invoice_name["+ i +"]' placeholder='Наименование' data-type='other' class='sumItg' onblur='func(this.id,this.value)' value='' id='n_"+ i +"'> " +
				"<input autocomplete='off' min='1' required type='number' name='count["+ i +"]' placeholder='Расход на производство (число)' data-type='other' onblur='func(this.id,this.value)' value='' id='n_"+ (i+1) +"'> " +
				"<input autocomplete='off' min='1' required type='number' name='cost["+ i +"]' placeholder='Цена (число)' class='test' data-type='other' onblur='func(this.id,this.value)' value='' id='n_"+ (i+2) +"'><span class='del'>&times;</span></div> " ).insertBefore("#form_status_added_other");

            document.getElementById("forprint").style="display: none";
            document.getElementById("save_data").style="display: none";
            document.getElementById("button_save").style="display: none";
		};


//
//function save_input_(){
//
//var vbbn = $("#localStorage_").html();
//
//localStorage.setItem('myKey', vbbn); //теперь у вас в localStorage хранится ключ "myKey" cо значением "myValue"
//
//alert('Введенные данные для расчёта себестоимости сохранены.');
////Выводим его в консоль:
////var localValue = localStorage.getItem('myKey');
//
////alert(localValue);
//
//};
//
//
//function output_input_(){
//
//document.getElementById("forprint").style="display: none";
////Выводим его в консоль:
//var localValue = localStorage.getItem('myKey');
//
////$("#block").html(localValue);
//
//$("#localStorage_").html(localValue);
//
//alert('Форма для расчёта себестоимости заполнена ранее сохранёнными данными.');
//
//};
//

//  function load_picture(){
//
//
//    //document.getElementById("forprint").style="width: 500";
//
//    $('#forprint').css({'width': '100%','padding':'10px'});
//
//    //alert('gdgsdg');
//
//    html2canvas($("#forprint"), {
//
//
//      onrendered: function (canvas) {
//        var a = document.createElement('a');
//        // toDataURL defaults to png, so we need to request a jpeg, then convert for file download.
//        a.href = canvas.toDataURL("image/png",1).replace("image/png", "image/octet-stream");
//        a.download = 'calculation.png';
//        a.click();
//      }
//
//    });
//
//
//  };

/* assign  attribut value input  */

    function func(a,b){
        //alert(a);
        //alert(b);
        $('#' + a ).attr('value', b);
    }

/* Получение выбранной валюты--------------------------------------------*/

    function status_option(a){

        var value = $('#currency').val();
        var select = document.querySelector('#currency').getElementsByTagName('option');

        for (let i = 0; i < select.length; i++) {
            if (select[i].value == value) {select[i].setAttribute('selected', '');}
            //select[i].selected = true;
        }
    };
