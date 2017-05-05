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

