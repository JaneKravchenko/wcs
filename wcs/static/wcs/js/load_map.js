
view = new ol.View({
          center: [0, 0],
          zoom: 2
        });
function transform(extent) {
        return ol.proj.transformExtent(extent, 'EPSG:4326', 'EPSG:3857');
      };
var container = document.getElementById('map');
var osm_lyr = new ol.layer.Tile({
            extent: transform([25.443582, 47.724953,35.710828, 50.4295349990001]),
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
        layers: [bm,osm_lyr
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
  var golosyyvski_source = new ol.source.TileWMS({
                 url: 'http://localhost:8080/geoserver/wcs/wms',
                 params: {
                     'LAYERS': 'wcs:wcs_national_park'
                 },
                 tiled: true
             });

             var tiled = new ol.layer.Tile({
                 source: golosyyvski_source
             });
map.addLayer(tiled);




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

function del_lyr(){
    $('#instruments').css('visibility', 'visible');
    $('#instruments_back').css('visibility', 'hidden');
    $('#instruments_back').css('height', '0');
    map.removeLayer(bm);
}

 

