jQuery(window).load(function($){
		if(jQuery(".lp_home").is("#homeMap")) {
		jQuery('#homeMap').empty();
		
			L.Google = L.Class.extend({
				includes: L.Mixin.Events,

				options: {
					minZoom: 0,
					maxZoom: 18,
					tileSize: 256,
					subdomains: 'abc',
					errorTileUrl: '',
					attribution: '',
					opacity: 1,
					continuousWorld: false,
					noWrap: false,
				},

				// Possible types: SATELLITE, ROADMAP, HYBRID
				initialize: function(type, options) {
					L.Util.setOptions(this, options);

					this._type = google.maps.MapTypeId[type || 'SATELLITE'];
				},

				onAdd: function(map, insertAtTheBottom) {
					this._map = map;
					this._insertAtTheBottom = insertAtTheBottom;

					// create a container div for tiles
					this._initContainer();
					this._initMapObject();

					// set up events
					map.on('viewreset', this._resetCallback, this);

					this._limitedUpdate = L.Util.limitExecByInterval(this._update, 150, this);
					map.on('move', this._update, this);
					//map.on('moveend', this._update, this);

					this._reset();
					this._update();
				},

				onRemove: function(map) {
					this._map._container.removeChild(this._container);
					//this._container = null;

					this._map.off('viewreset', this._resetCallback, this);

					this._map.off('move', this._update, this);
					//this._map.off('moveend', this._update, this);
				},

				getAttribution: function() {
					return this.options.attribution;
				},

				setOpacity: function(opacity) {
					this.options.opacity = opacity;
					if (opacity < 1) {
						L.DomUtil.setOpacity(this._container, opacity);
					}
				},

				_initContainer: function() {
					var tilePane = this._map._container
						first = tilePane.firstChild;

					if (!this._container) {
						this._container = L.DomUtil.create('div', 'leaflet-google-layer leaflet-top leaflet-left');
						this._container.id = "_GMapContainer";
					}

					if (true) {
						tilePane.insertBefore(this._container, first);

						this.setOpacity(this.options.opacity);
						var size = this._map.getSize();
						this._container.style.width = size.x + 'px';
						this._container.style.height = size.y + 'px';
					}
				},

				_initMapObject: function() {
					this._google_center = new google.maps.LatLng(0, 0);
					var map = new google.maps.Map(this._container, {
						center: this._google_center,
						zoom: 0,
						mapTypeId: this._type,
						disableDefaultUI: true,
						keyboardShortcuts: false,
						draggable: false,
						disableDoubleClickZoom: true,
						scrollwheel: false,
						streetViewControl: false
					});

					var _this = this;
					this._reposition = google.maps.event.addListenerOnce(map, "center_changed", 
						function() { _this.onReposition(); });
				
					map.backgroundColor = '#ff0000';
					this._google = map;
				},

				_resetCallback: function(e) {
					this._reset(e.hard);
				},

				_reset: function(clearOldContainer) {
					this._initContainer();
				},

				_update: function() {
					this._resize();

					var bounds = this._map.getBounds();
					var ne = bounds.getNorthEast();
					var sw = bounds.getSouthWest();
					var google_bounds = new google.maps.LatLngBounds(
						new google.maps.LatLng(sw.lat, sw.lng),
						new google.maps.LatLng(ne.lat, ne.lng)
					);
					var center = this._map.getCenter();
					var _center = new google.maps.LatLng(center.lat, center.lng);

					this._google.setCenter(_center);
					this._google.setZoom(this._map.getZoom());
					this._google.fitBounds(google_bounds);
				},

				_resize: function() {
					var size = this._map.getSize();
					if (this._container.style.width == size.x &&
						this._container.style.height == size.y)
						return;
					this._container.style.width = size.x + 'px';
					this._container.style.height = size.y + 'px';
					google.maps.event.trigger(this._google, "resize");
				},

				onReposition: function() {
					//google.maps.event.trigger(this._google, "resize");
				}
			});

			L.HtmlIcon = L.Icon.extend({
				options: {
					/*
					html: (String) (required)
					iconAnchor: (Point)
					popupAnchor: (Point)
					*/
				},

				initialize: function(options) {
					L.Util.setOptions(this, options);
				},

				createIcon: function() {
					var div = document.createElement('div');
					div.innerHTML = this.options.html;
					if (div.classList)
						div.classList.add('leaflet-marker-icon');
					else
						div.className += ' ' + 'leaflet-marker-icon';
					return div;
				},

				createShadow: function() {
					return null;
				}
			});
			
			
			
			
			
			
			jQuery.ajax({
				type: 'POST',
				dataType: 'json',
				url: listingpro_home_map_object.ajaxurl,
				data: { 
					'action': 'listingpro_home_map_content', 
					'trig': 'home_map', 
					},
				success: function(data){
					if(data){
						jQuery('#homeMap').addClass('loading');
						var map = null
						$mtoken = jQuery('#page').data("mtoken");	
						$mapboxDesign = jQuery('#page').data("mstyle");
						if($mtoken != ''){
						
							L.mapbox.accessToken = $mtoken;
							 map = L.mapbox.map('homeMap', 'mapbox.streets');
							L.tileLayer('https://api.tiles.mapbox.com/v4/'+$mapboxDesign+'/{z}/{x}/{y}.png?access_token='+$mtoken+'', {
										maxZoom: 18,
										attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
											'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
											'Imagery © <a href="http://mapbox.com">Mapbox</a>',
										id: 'mapbox.light'
							}).addTo(map);						
							 
							var markers = new L.MarkerClusterGroup();
							
							jQuery.each(data, function(i,v) { 
								if(v.latitude != null && v.longitude != null){
								if(v.latitude != '' && v.longitude != ''){
									//alert(v.latitude);
									var markerLocation = new L.LatLng(v.latitude, v.longitude); // London

									var CustomHtmlIcon = L.HtmlIcon.extend({
										options : {
											html : "<div class='lpmap-icon-shape pin card"+i+"'><div class='lpmap-icon-contianer'><img src='"+v.icon+"' /></div></div>",
										}
									});

									var customHtmlIcon = new CustomHtmlIcon(); 

									var marker = new L.Marker(markerLocation, {icon: customHtmlIcon}).bindPopup('<div class="map-post"><div class="map-post-thumb"><a target="_blank" href="'+v.url+'">'+v.image+'</a></div><div class="map-post-des"><div class="map-post-title"><h5><a target="_blank" href="'+v.url+'">'+v.title+'</a></h5></div><div class="map-post-address"><p><i class="fa fa-map-marker"></i> '+v.address+'</p></div></div></div>').addTo(map);
									markers.addLayer(marker);
									map.addLayer(markers);
								}
								}
							});
							
							
							map.fitBounds(markers.getBounds());
							
							map.scrollWheelZoom.disable();
						}else{
							//var map = new L.Map('homeMap', '');
							var map = new L.Map('homeMap', {
							   dragging: false,
							   tap: false
							});
							
							var googleLayer = new L.Google('ROADMAP');						
							map.addLayer(googleLayer);
							var markers = new L.MarkerClusterGroup();	

							jQuery.each(data, function(i,v) { 
								if(v.latitude != null && v.longitude != null){
								if(v.latitude != '' && v.longitude != ''){
									//alert(v.latitude);
									var markerLocation = new L.LatLng(v.latitude, v.longitude); // London

									var CustomHtmlIcon = L.HtmlIcon.extend({
										options : {
											html : "<div class='lpmap-icon-shape pin card"+i+"'><div class='lpmap-icon-contianer'><img src='"+v.icon+"' /></div></div>",
										}
									});

									var customHtmlIcon = new CustomHtmlIcon(); 

									var marker = new L.Marker(markerLocation, {icon: customHtmlIcon}).bindPopup('<div class="map-post"><div class="map-post-thumb"><a target="_blank" href="'+v.url+'">'+v.image+'</a></div><div class="map-post-des"><div class="map-post-title"><h5><a target="_blank" href="'+v.url+'">'+v.title+'</a></h5></div><div class="map-post-address"><p><i class="fa fa-map-marker"></i> '+v.address+'</p></div></div></div>').addTo(map);
									markers.addLayer(marker);
									map.addLayer(markers);
								}
								}
							});
							

							map.fitBounds(markers.getBounds());
							
							map.scrollWheelZoom.disable();
							map.invalidateSize();
						}
					}
					
								
					
					
						

				}
			});
			
			
			
			
			
			
			
		}
	});