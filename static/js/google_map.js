

function getLocation(){
    if (window.current_location){
        return window.current_location;
    }
    else{
        setLocation();
        return window.current_location;
    }
}


function setLocation(){
    jQuery.ajax(
        {
        url:window.ip_track_url,
        method: "GET",
        async:false,
        dataType: "json",
        success: function(location) {
            lat_long = location.loc.split(",");
            location.loc = {}
            location.loc.latitude = parseFloat(lat_long[0]);
            location.loc.longitude = parseFloat(lat_long[1]);
            window.current_location = location;
        }
});
}


function setGoogleMapMarkers(listing_data){
    /***

    e.g.
    var listing_data = [
          {id: 12, name:'Bondi Beach', latitude:-33.890542, longitude:151.274856},
          {name:'Coogee Beach', latitude:-33.923036, longitude:151.259052},
          {name:'Cronulla Beach', latitude:-34.028249, longitude:151.157507},
          {name:'Manly Beach', latitude:-33.80010128657071, longitude:151.28747820854187},
          {name:'Maroubra Beach', latitude:-33.950198, longitude:151.259302}
    ];

    ***/
    if (! listing_data){
        listing_data = window.listing_data || [];
    }

    if (! listing_data.length){
        return false;
    }

    var infowindow = new google.maps.InfoWindow();

    var cur_loc = getLocation().loc;


    cur_loc_info = {name: 'You are currently here', latitude:cur_loc.latitude, longitude: cur_loc.longitude};
    listing_data.splice(0, 0, cur_loc_info);

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 10,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        //center:
        panControl: true,
        zoomControl: true,
        zoomControlOptions: {
              position: google.maps.ControlPosition.LEFT_TOP
        },
        mapTypeControl: true,
        scaleControl: true,
        streetViewControl: true,
        streetViewControlOptions: {
              position: google.maps.ControlPosition.LEFT_TOP
        },
        overviewMapControl: true,
        rotateControl: true
    });


    var marker, i;
    all_markers = []
    for (i = 0; i < listing_data.length; i++) {

      var lat = listing_data[i].latitude;
      var lng = listing_data[i].longitude
      console.warn([lat, lng]);
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(lat, lng),
        map: map,
        animation: google.maps.Animation.DROP
      });
      if (listing_data[i].id){
            marker_html = mapListingPopover(listing_data[i].id, listing_data[i].name, listing_data[i].address, listing_data[i].banner_photo);
      }
      else{
            marker_html = listing_data[i].title;
      }
      marker.marker_html = marker_html;
      google.maps.event.addListener(infowindow, "closeclick", function(){
        map.setZoom(10);
      });

      google.maps.event.addListener(marker, 'click', (function(marker, i) {
        return function() {
          infowindow.setContent(marker.marker_html);
          infowindow.open(map, marker);
          map.setZoom(11);
          map.setCenter(marker.getPosition());
        }
      })(marker, i));
      all_markers.push(marker);
    }
    if (marker){
        map.setCenter(marker.getPosition());
    }
    else{
        map.setCenter({lat:cur_loc_info.latitude, lng:cur_loc_info.longitude});
    }
}

function mapListingPopover(id, title, address, img_url){
    var detail_url = "/business/detail/"+id;
    if (img_url && img_url.indexOf('/media/')!=0){
        img_url = '/media/'+img_url;
    }
    var html = '<div style="width: 250px;"><div><a href="'+detail_url+'"><img style="width:100%;height:100%" src="'+img_url+'" ></a></div><div><div class="map-post-title"><h5><a href="'+detail_url+'">'+title+'</a></h5></div><div class="map-post-address"><p><i class="fa fa-map-marker"></i> '+address+'</p></div></div></div>'
    return html
}


//function clearCurrentMarkers(){
//    gmap = getGoogleMap();
//    if (window.current_markers){
//        for (var i = 0; i < markers.length; i++) {
//          markers[i].setMap(map);
//        }
//    }
//}


