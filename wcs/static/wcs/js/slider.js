$( "#slider" ).slider({
				value : 50.0,//Значение, которое будет выставлено слайдеру при загрузке
				min : 0,//Минимально возможное значение на ползунке
				max : 500,//Максимально возможное значение на ползунке
				step : 0.01,//Шаг, с которым будет двигаться ползунок
				create: function( event, ui ) {
					val = $( "#slider" ).slider("value");//При создании слайдера, получаем его значение в перемен. val
					$( "#contentSlider" ).html( val);//Заполняем этим значением элемент с id contentSlider



				},
            slide: function( event, ui ) {
				$( "#contentSlider" ).html( ui.value);//При изменении значения ползунка заполняем элемент с id contentSlider
                radius = ui.value;



            }
});


$( "#slider_transparent" ).slider({
				value : 0,//Значение, которое будет выставлено слайдеру при загрузке
				min : 0,//Минимально возможное значение на ползунке
				max : 100,//Максимально возможное значение на ползунке
				step : 0.01,//Шаг, с которым будет двигаться ползунок
				create: function( event, ui ) {
					val = $( "#slider_transparent" ).slider("value");//При создании слайдера, получаем его значение в перемен. val
					$( "#contentSlider_transparent" ).html( val);//Заполняем этим значением элемент с id contentSlider



				},
            slide: function( event, ui ) {
				$( "#contentSlider_transparent" ).html( ui.value);//При изменении значения ползунка заполняем элемент с id contentSlider
                name = $('#all_lyr').val();
                console.log(name);
                for (i = 0; i < map.getLayers().getArray().length; i++) {
                	if (map.getLayers().getArray()[i].get('name') === name){
                		map.getLayers().getArray()[i].setOpacity(1-ui.value/100);
                		console.log(ui.value/100);
                	}
                };



            }
});
