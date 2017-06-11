
view = new ol.View({
          center: [3608691.0429451764,6678080.323315691],
          zoom: 14
        });


function transform(extent) {
        return ol.proj.transformExtent(extent, 'EPSG:4326', 'EPSG:3857');
      };
var container = document.getElementById('map');

var osm_lyr = new ol.layer.Tile({
  name: 'Open_Street_Map',
            source: new ol.source.OSM()
          });
var bm = new ol.layer.Tile({
          visible: true,
          preload: Infinity,
          source: new ol.source.BingMaps({
            key: 'Ag79SHcZN9PeuuOr5TekKDaUGskx0aTCrjANtTU1Y51xczDomXooCme3d5TquH5A',
            imagerySet: 'AerialWithLabels'

          })
        });
      var map = new ol.Map({
        layers: [osm_lyr
        ],

        target: container,

        view: view
      });
             var ovm = new ol.control.OverviewMap();
             var scaleline = new ol.control.ScaleLine();
             var zoomslider = new ol.control.ZoomSlider();
             var zoo = new ol.control.Zoom();



       var map2 = new ol.Map({
        layers: [osm_lyr
        ],
        target: 'map2',

        view: view
      });





             var control1 = new  ol.control.FullScreen();

             map.addControl(control1);


             map.addControl(ovm);
             map.addControl(scaleline);
             map.addControl(zoomslider);
             map.addControl(zoo);
var radius = 50;
function ad_lyr(){
    $('#instruments').css('visibility', 'hidden');
    $('#instruments_back').css('visibility', 'visible');
    $('#instruments_back').css('height', '100px');
    map.addLayer(bm);

      document.addEventListener('keydown', function(evt) {
        if (evt.which === 38) {
          radius = Math.min(radius + 5, 150);
          map.render();
          evt.preventDefault();
        } else if (evt.which === 40) {
          radius = Math.max(radius - 5, 25);
          map.render();
          evt.preventDefault();
        }
      });


      // get the pixel position with every move
      var mousePosition = null;

      container.addEventListener('mousemove', function(event) {
        mousePosition = map.getEventPixel(event);
        map.render();
      });

      container.addEventListener('mouseout', function() {
        mousePosition = null;
        map.render();
      });

      // before rendering the layer, do some clipping
      bm.on('precompose', function(event) {
        var ctx = event.context;
        var pixelRatio = event.frameState.pixelRatio;

        ctx.save();

        ctx.beginPath();
        if (mousePosition) {
          // only show a circle around the mouse
          ctx.arc(mousePosition[0] * pixelRatio, mousePosition[1] * pixelRatio,
              radius * pixelRatio, 0, 2 * Math.PI);
          ctx.lineWidth = 5 * pixelRatio;
          ctx.strokeStyle = 'rgba(0,0,0,0.5)';
          ctx.stroke();
        }
        ctx.clip();

      });

      // after rendering the layer, restore the canvas context
      bm.on('postcompose', function(event) {
        var ctx = event.context;
        ctx.restore();
      });}

INSTRUMENTS = ['#instruments_back', '#instruments_transparent'];


/*
Кнопка Н А З А Д
*/
function hidden_instruments(name){
 $(name).css('visibility', 'hidden');
 $(name).css('height', '0');
};


/*
Кнопка П Р О З О Р І С Т Ь
*/
function transparent_lyr(){
  document.getElementById('all_lyr').innerHTML = ' ';
  for (i = 0; i < map.getLayers().getArray().length; i++) {
  
    document.getElementById('all_lyr').innerHTML += '<option value = "'+(map.getLayers().getArray())[i].get('name')+'">' + (map.getLayers().getArray())[i].get('name')+ '</option>';
}


   $('#instruments').css('visibility', 'hidden');
   $('#instruments_transparent').css('visibility', 'visible');
   $('#instruments_transparent').css('height', '100px');
}

/*
Кнопка Н А З А Д
*/
function del_lyr(){
    $('#instruments').css('visibility', 'visible');
    for (i in INSTRUMENTS){
      hidden_instruments(INSTRUMENTS[i]);
    };

    map.removeLayer(bm);
}

function load_dem(){
var tiled = new ol.layer.Tile({
        visible: true,
        source: new ol.source.TileWMS({
          url: 'http://localhost:8080/geoserver/cite/wms',
          params: {'FORMAT': 'image/png', 
                   'VERSION': '1.1.1',
                   tiled: true,
                STYLES: '',
                LAYERS: 'cite:n48_e023_1arc_v3(1)',
             tilesOrigin: 27.999861111111112 + "," + 47.99986111111111
          }
        })
      });

map.addLayer(tiled);


view.setCenter(ol.proj.fromLonLat([23.2567, 48.529]));
view.setZoom(9);
document.getElementById('modal-body').innerHTML+='<div class="progress"><div class="progress-bar progress-bar-striped active" role="progressbar" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100" style="width: 45%"><span class="sr-only">45% Complete</span></div></div>'
setTimeout($('#btn_close').click(), 10000000000);
}


function parse_json(){
    jso = document.getElementById('geometry').innerHTML;


        var format = new ol.format.WKT();

      var feature = format.readFeature(jso, {
        dataProjection: 'EPSG:4326',
        featureProjection: 'EPSG:3857'
      });

      var vector = new ol.layer.Vector({
        source: new ol.source.Vector({
          features: [feature]
        })
      });

      map.addLayer(vector);
      console.log('add layer');






}




function check_check(id){
    $('input:checkbox').change(function() {
        // this will contain a reference to the checkbox
        list_of_lyr = map.getLayers().getArray();
        list_of_lyr_name = [];
        for (i = 0; i < list_of_lyr.length; i++) {
            list_of_lyr_name.push(list_of_lyr[i].get('name'));
        }
        if (this.checked) {
            console.log(this.value);
            var value = this.value;
            if (list_of_lyr_name.indexOf(value) != -1) {
                list_of_lyr[list_of_lyr_name.indexOf(value)].setVisible(true);
            }

      } else {
                var value = this.value;

list_of_lyr[list_of_lyr_name.indexOf(value)].setVisible(false);

 };


    });
}


function remove_layer(name){
  for (i in map.getLayers().getArray()){
    if (map.getLayers().getArray()[i].get('name')===name){
      console.log(map.getLayers().getArray()[i].get('name'));
      map.removeLayer(map.getLayers().getArray()[i]);
    }
  }
  el = document.getElementById(name+'2');
  el.parentNode.removeChild(el);
  $('#'+name).css('color', 'rgba(0,0,0,0.7)');
  $('#'+name).css('background-color', 'rgba(255,255,255,0)');
  $('#'+name).prop('disabled',false);

}

function remove_map(){
  for (i in map.getLayers().getArray()){
    if (map.getLayers().getArray()[i].get('name')!=='Open_Street_Map'){
      var name = map.getLayers().getArray()[i].get('name');
      map.removeLayer(map.getLayers().getArray()[i]);
el = document.getElementById(name+'2');
  el.parentNode.removeChild(el);

  $('#'+name).css('color', 'rgba(0,0,0,0.7)');
  $('#'+name).css('background-color', 'rgba(255,255,255,0)');
  $('#'+name).prop('disabled',false);
    }
  }

}


function information_point(){


      var source = new ol.source.Vector({wrapX: false});

      var vector = new ol.layer.Vector({
        source: source
      });

       var typeSelect = 'Point';

      var draw; // global so we can remove it later
      function addInteraction() {
        var value = 'Point';
        if (value !== 'None') {
          draw = new ol.interaction.Draw({
            source: source,
            type: /** @type {ol.geom.GeometryType} */ ('Point')
          });
          map.addInteraction(draw);
        }
      }


      /**
       * Handle change event.
       */
      typeSelect.onchange = function() {
        map.removeInteraction(draw);
        addInteraction();
      };

      addInteraction();
         var container = document.getElementById('popup');
      var content = document.getElementById('popup-content');
      var closer = document.getElementById('popup-closer');


      /**
       * Create an overlay to anchor the popup to the map.
       */
     
 var overlay = new ol.Overlay(/** @type {olx.OverlayOptions} */ ({
        element: container,
        autoPan: true,
        autoPanAnimation: {
          duration: 250
        }
      }));
 map.addOverlay(overlay);
      /**
       * Add a click handler to hide the popup.
       * @return {boolean} Don't follow the href.
       */
      closer.onclick = function() {
        overlay.setPosition(undefined);
        closer.blur();
        return false;
      };




      map.on('click', function(evt) {
        if (source.getFeatures().length == 1){
          geojson = new ol.format.GeoJSON();
          var str = geojson.writeFeatures(source.getFeatures(), true);
          $.ajax({
                 url: "inform_point",
                 type: "GET",
                 data: str,
                 async: false,
                 success: function(response) {
                    content.innerHTML=response;
                    console.log(response);
                 },
                 complete: function(xhr, status) {
                 },
                 error: function(xhr, textStatus, thrownError) {
                     console.log(thrownError);
                 }
             });
         
          source.clear();
map.removeInteraction(draw);

var coordinate = evt.coordinate;
        var hdms = ol.coordinate.toStringHDMS(ol.proj.transform(
            coordinate, 'EPSG:3857', 'EPSG:4326'));

        
        overlay.setPosition(coordinate);
        };

      
});


}


