
WebFontConfig = {
  google: {
    families: [ 'Open Sans:300,400,500,600,700:latin' ]
  },
  active: function() {
    //jQuery(window).trigger("debouncedresize");
  }
};
(function() {
  var wf = document.createElement('script');
  wf.src = ('https:' == document.location.protocol ? 'https' : 'http') +
  '://ajax.googleapis.com/ajax/libs/webfont/1/webfont.js';
  wf.type = 'text/javascript';
  wf.async = 'true';
  var s = document.getElementsByTagName('script')[0];
  s.parentNode.insertBefore(wf, s);
})();



function initializeMap() {
  var $mapDiv = $('#business-map');
  var mapPosn = $mapDiv.data('business-location').split(',');
  var latLngPosn = new google.maps.LatLng(mapPosn[0], mapPosn[1]);
  var map = new google.maps.Map(document.getElementById($mapDiv.attr('id')), {
    center: latLngPosn,
    zoom: 15,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });
  var marker = new google.maps.Marker({
    position: latLngPosn,
    map: map,
    title: $mapDiv.data('title')
  });

  // Reposition on resize.
  google.maps.event.addDomListener(window, 'resize', function() {
    map.setCenter(latLngPosn);
  });
}

function loadMapScript() {
  var MAP_API_KEY='AIzaSyC0R7ZCp3WupbjWoK1xnFcYArwvZ0gD7Ks';
  var script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = 'https://maps.googleapis.com/maps/api/js?key=' + MAP_API_KEY + '&callback=initializeMap';
  document.body.appendChild(script);
}

var africaOne = {};

//home page
africaOne.initiateHomePage = function() {

  //check for home page wrapper
  var $homePageWrapper = $('.home-page-wrapper.full-page-wrapper');
  if ($homePageWrapper.length <= 0) return;

  //banner slider
  africaOne.initiateHomeBannerSlides();

};


/**
 * set up banners
 */
africaOne.initiateHomeBannerSlides = function() {
  var $bannerWrapper = $('.home-banner-reviews-wrapper');
  var $bannersList = $('.home-banner-reviews', $bannerWrapper);
  var location = {
    latitude: 0,
    longitude: 0
  };
  var geoOptions = {
    maximumAge: 5 * 60 * 1000,
    timeout: 10 * 1000
  };

  var getBanners = function() {
    $.get('/get_nearest_businesses/', {
      latitude: location.latitude,
      longitude: location.longitude
    }).done(function (bannerData) {
      console.log(bannerData);
      setupBanners(bannerData);
    });
  };

  var setupBanners = function(bannerData) {
    var $bannerItem = $('.banner-review-html-holder', $bannersList).remove();
    $.each(bannerData, function(index, bannerInfo) {
      var $newBannerItem = $bannerItem.clone().removeClass('banner-review-html-holder');
      $newBannerItem.addClass('banner-review-' + index);
      $newBannerItem.css('background-image', 'url("' + bannerInfo.bannerImgURL + '")');
      $('.business-img', $newBannerItem).css('background-image', 'url("' + bannerInfo.logoURL + '")');
      $('h2', $newBannerItem).text(bannerInfo.cityName + ' awaits your review');
      $('.txt .name', $newBannerItem).text(bannerInfo.businessName + '?');
      $('.business-rating h2', $newBannerItem).text(bannerInfo.businessName);
      $('.business-id', $newBannerItem).val(bannerInfo.businessID);
      $newBannerItem.appendTo($bannersList);
    });
    setupBannerSlider();
  };

  var setupBannerSlider = function() {
    //create content desc on top
    var $bannerDesc = $('.banner-review-desc', $bannersList).first().clone();
    $bannerDesc.appendTo($bannerWrapper).addClass('all-banner-desc');
    $('.banner-review-desc', $bannersList).hide();

    //set up banner slider
    var bannerSlider = $bannerWrapper.unslider({
      autoplay: true,
      arrows: false,
      infinite: true,
      delay: 10000
    });
    $('.banner-review-start', $bannerWrapper).append('<div class="banners-arrow"><div class="slider-btn slider-btn-prev"><div class="arrow grey"></div><div class="arrow white"></div></div><div class="slider-btn slider-btn-next"><div class="arrow grey"></div><div class="arrow white"></div></div></div>');
    $('.slider-btn-next', $bannerWrapper).click ( function() {
      bannerSlider.unslider('next');
    });
    $('.slider-btn-prev', $bannerWrapper).click ( function() {
      bannerSlider.unslider('prev');
    });
    bannerSlider.on('unslider.change', function(event, index, $slide) {
      var $comingDesc = $('.banner-review-desc', $slide);
      $('.business-img', $bannerDesc).css('background-image', $('.business-img', $comingDesc).css('background-image'));
      $('.txt .name', $bannerDesc).text($('.txt .name', $comingDesc).text());
      $('.business-rating h2', $bannerDesc).text($('.business-rating h2', $comingDesc).text());
      $('.business-id', $bannerDesc).val($('.business-id', $comingDesc).val());
    });

    //move to higher in dom
    $bannerDesc.appendTo($bannerWrapper.closest('.unslider'));

    //initiate review stars
    africaOne.initiateReviewerStars();

    //watch out for review events
    var $startReviewStars = $('.star-rating-widget', $bannerDesc);
    $startReviewStars.on('africaone:start_review_started', function() {
      bannerSlider.unslider('stop');
      $('.slider-btn', $bannerDesc).hide();
      $('.home-page-wrapper .unslider-nav').hide();
    });
    $startReviewStars.on('africaone:start_review_cancelled', function() {
      bannerSlider.unslider('start');
      $('.slider-btn', $bannerDesc).show();
      $('.home-page-wrapper .unslider-nav').show();
    });

    //banner form
    africaOne.initiateBannerReviewForm();

  };

  var geoSuccess = function(position) {
    location.latitude = position.coords.latitude;
    location.longitude = position.coords.longitude;
    //getBanners();
    setupBannerSlider();
  };

  var geoError = function(position) {
    getBanners();
  };

  navigator.geolocation.getCurrentPosition(geoSuccess, geoError, geoOptions);
};


/**
 * prepare AJAX calls with CSRF token
 */
africaOne.prepareAjaxCalls = function() {
  var getCookie = function (name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?

        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      }
    }
  });
};


/**
 * home page review form
 */
africaOne.initiateBannerReviewForm = function() {
  var $form = $('.home-page-wrapper .all-banner-desc .start-review-form');
  var $startReviewStars = $('.star-rating-widget', $form);
  var $textarea = $('textarea', $form);

  //watch for textarea focus
  $textarea.focus( function() {
    if (!$form.hasClass('form-active')) {
      $startReviewStars.trigger('africaone:start_review_started');
    }
  });

  //watch for start and cancel of review
  $startReviewStars.on('africaone:start_review_started', function() {
    $form.addClass('form-active').removeClass('form-error');
  });
  $startReviewStars.on('africaone:start_review_cancelled', function() {
    $textarea.val('');
    $form.removeClass('form-active');
  });

  //cancel button
  $('.cancel-review', $form).click( function() {
    $startReviewStars.trigger('africaone:start_review_cancelled')
  });

  //submit button
  $form.submit( function() {
    if ($.trim($textarea.val()) == '' || $('input[name="rating"]:checked').length <= 0) {
      $form.addClass('form-error');
      return false;
    } else {
      $form.removeClass('form-error');
      return true;
    }
  });
};


/**
 * prepare active review stars
 */
africaOne.initiateReviewerStars = function() {
  var resetStars = function($ul, $description) {
    $ul.removeClass(function (index, css) {
      return (css.match(/(^|\s)stars-\S+/g) || []).join(' ');
    });
    $description.text('Select a rating');
    $('input[name="rating"]', $ul).prop('checked', false);
  };

  $('.star-rating-widget').each( function (index, elem) {
    var $starsWrapper = $(elem);
    var $description = $('.rating-description', $starsWrapper);
    var $ul = $('.rating-stars', $starsWrapper);
    $starsWrapper.data('form-active', false);
    $('.rating-star-li', $ul).each( function (index, li) {
      var $li = $(li);
      var $label = $('label', $li);
      $li.hover(
        function() {
          if (!$starsWrapper.data('form-active')) {
            resetStars($ul, $description);
            $ul.addClass('stars-' + (index + 1));
            $description.text($label.text());
          }
        },
        function() {
          if (!$starsWrapper.data('form-active')) {
            resetStars($ul, $description);
          }
        }
      );
      $li.click( function () {
        $starsWrapper.data('form-active', true);
        $starsWrapper.trigger('africaone:start_review_started')
      });
    });
    $starsWrapper.on('africaone:start_review_cancelled', function() {
      $starsWrapper.data('form-active', false);
      resetStars($ul, $description);
    });
  });

};


/**
 * set up fancy checkboxes
 */
africaOne.setUpFancyCheckboxes = function() {

  //filter checkboxes
  $('.filters-col input, input.fancy-checkbox').iCheck({
    checkboxClass: 'icheckbox_square-green',
    radioClass: 'iradio_square-green',
    increaseArea: '20%' // optional
  });

};


/**
 * set up chosen selects
 */
africaOne.setUpChosenSelects = function() {
  $('select.chosen-select').chosen({
    width: '100%'
  });

  var $eventCategoriesSelect = $('select#event-categories');
  $eventCategoriesSelect.chosen({
    width: '100%',
    max_selected_options: 3
  });
  $eventCategoriesSelect.bind("", function() {
    alert('You can only pick a maximum of three categories.');
  });
};


/**
 * set up location chooser
 */
africaOne.setUpLocationChooser = function() {
  var $mapWrappers = $('.location-finder');
  $mapWrappers.each( function(index, elem) {
    var $wrapper = $(elem);
    var $searchTextWrapper = $('.location-search-field', $wrapper);
    var $searchBtn = $('.form-btn', $searchTextWrapper);
    var $searchInput = $('input.form-text', $searchTextWrapper);

    $searchInput.on("keypress", function(e) {
      if (e.keyCode == 13) {
        $searchBtn.click();
        return false; // prevent the button click from happening
      }
    });

  });
};


$(window).ready( function() {

  //prepare ajax calls
  //africaOne.prepareAjaxCalls();

  //call maps when dom ready
  if ($('#business-map').length) {
    loadMapScript();
  }

  //look for infield labels
  var $infieldLabelForms = $(".infield-labels").addClass('labels-in-field');
  $("label", $infieldLabelForms).inFieldLabels();
  $('input', $infieldLabelForms).attr('placeholder', '');

  //home page
  africaOne.initiateHomePage();

  //review stars
  africaOne.initiateReviewerStars();

  //fancy checkboxes and selects
  africaOne.setUpFancyCheckboxes();
  africaOne.setUpChosenSelects();
  africaOne.setUpLocationChooser();

  //body js class
  $('body').addClass('js-ready');

});
