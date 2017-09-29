
var africaone = {};

/**
 * businesses list
 */
africaone.initiateBusinesses = function() {
  var $wrapper = $('.africaone-home-wrapper .businesses-list');
  if ($wrapper.length <= 0) {
    return;
  }

  var $listItemsWrapper = $('.businesses-list-items-wrapper', $wrapper);
  var $detailsItemsWrapper = $('.businesses-full-details-wrapper', $wrapper);

  $('.business-list-item', $listItemsWrapper).click( function() {
    var $businessItem = $(this);
    var businessID = $businessItem.data('id');

    $('.business-list-item', $listItemsWrapper).removeClass('active');
    $businessItem.addClass('active');

    $('.business-full-detail-wrapper', $detailsItemsWrapper).hide();
    $('#business-full-detail-' + businessID, $detailsItemsWrapper).show();

    $wrapper.addClass('showing-details');
  });

  $('.close-btn-col .btn', $detailsItemsWrapper).click( function() {
    $wrapper.removeClass('showing-details');
    $('.business-full-detail-wrapper', $detailsItemsWrapper).hide();
  });

};


/**
 * validate form
 */
africaone.initialiseBusinessForm = function() {
  var $form = $('form#create-business-form');

  if ($form.length <= 0) return;

  /*
  $form.attr('novalidate', 'novalidate');

  // initialize the validator function
  //validator.message['date'] = 'not a real date';

  // validate a field on "blur" event, a 'select' on 'change' event & a '.reuired' classed multifield on 'keyup':
  $form
      .on('blur', 'input[required], input.optional, select.required', validator.checkField)
      .on('change', 'select.required', validator.checkField)
      .on('keypress', 'input[required][pattern]', validator.keypress);

  $('.multi.required', $form)
      .on('keyup blur', 'input', function () {
        validator.checkField.apply($(this).siblings().last()[0]);
      });

  $form.submit(function (e) {
    e.preventDefault();
    var submit = true;
    var $this = $(this);
    if (!validator.checkAll($(this))) {
      submit = false;
    }
    if (submit)
      this.submit();
    return false;
  });

  //on form submit
  $form.submit(function (e) {
    e.preventDefault();
    var submit = true;
    var $form = $(this);
    if (!validator.checkAll($form)) {
      submit = false;
    }
    if (submit)
      this.submit();
    return false;
  });
  */

  //hours functionality
  var $hoursDisplayWrapper = $('.hours-wrapper', $form);
  var $hoursElem = $('.hours.hidden', $hoursDisplayWrapper).detach().removeClass('hidden');
  var $hoursForm = $('.hours-select', $form);
  var $weekdaySelect = $('.weekday', $hoursForm);
  var $startHourSelect = $('.hours-start', $hoursForm);
  var $endHourSelect = $('.hours-end', $hoursForm);
  var hoursArrayCounter = 0;
  $('.btn', $hoursForm).click( function() {
    var $newHoursElem = $hoursElem.clone();
    $('.weekday', $newHoursElem).text($('option:selected', $weekdaySelect).text());
    $('.start', $newHoursElem).text($('option:selected', $startHourSelect).text());
    $('.end', $newHoursElem).text($('option:selected', $endHourSelect).text());
    $('input', $newHoursElem).val($weekdaySelect.val() + ' ' + $startHourSelect.val() + ' ' + $endHourSelect.val()).attr('name', 'hours[' + hoursArrayCounter++ + ']');
    $('.remove-hours', $newHoursElem).click( function() {
      $newHoursElem.remove();
      return false;
    });
    var $nextOption = $('option:selected', $weekdaySelect).next();
    $newHoursElem.appendTo($hoursDisplayWrapper);
    if ($nextOption.length <= 0) {
      $nextOption = $('option:first-child', $weekdaySelect);
    }
    $weekdaySelect.val($nextOption.attr('value'));
    //$nextOption.attr('selected', 'selected'); //not working after first loop
  });

  //phone mask
  //$('#business-phone', $form).inputmask();

  //autocomplete categories
  var $categoriesSelect = $('#business-category', $form);
  var $chosenCategoriesWrapper = $('.chosen-categories-wrapper', $form);
  var $chosenCategoryElem = $('.chosen-category.hidden', $chosenCategoriesWrapper).detach().removeClass('hidden');
  var arrow = '<i class="category-spacer fa fa-angle-right"></i>';
  var categoriesArrayCounter = $('.chosen-category', $chosenCategoriesWrapper).length;
  categoriesArrayCounter = categoriesArrayCounter > 0 ? (categoriesArrayCounter-1) : 0;
  var checkMaxCategoriesNo = function() {
    var maxNo = 3;
    if ($('.chosen-category', $chosenCategoriesWrapper).length >= maxNo) {
      $categoriesSelect.prop('disabled', true);
    } else {
      $categoriesSelect.prop('disabled', false);
    }
  };
  var removeCategoryButton = function($wrapper) {
    $('.remove-category', $wrapper).click( function() {
      $wrapper.remove();
      checkMaxCategoriesNo();
      return false;
    });
  };
  $('.chosen-category', $chosenCategoriesWrapper).each( function (index, elem) {
    removeCategoryButton($(elem));
  });
  $categoriesSelect.autocomplete({
    serviceUrl: '/manager/get_categories',
    appendTo: '#categories-autocomplete-container',
    showNoSuggestionNotice: true,
    noSuggestionNotice: 'No categories found with this criteria. Please try again.',
    beforeRender: function(container) {
      $('.autocomplete-suggestion', $(container)).each( function(index, elem) {
        var $row = $(elem);
        $row.html($row.html().replace(' > ', arrow));
      });
    },
    onSelect: function (suggestion) {
      var $newChosenCategoryElem = $chosenCategoryElem.clone();
      $('span', $newChosenCategoryElem).html(suggestion.value.replace(' > ', arrow));
      $('input', $newChosenCategoryElem).val(suggestion.data).attr('name', 'categories[' + categoriesArrayCounter++ + ']');
      $newChosenCategoryElem.appendTo($chosenCategoriesWrapper);
      removeCategoryButton($newChosenCategoryElem);
      checkMaxCategoriesNo();
      $categoriesSelect.val('').focus();
    }
  });

  //map latitude and longitude picker
  var $mapWrapper = $('#business-location-map', $form);
  var $searchBtn = $('.search-btn', $form);
  var $locationDiv = $('.business-location-name', $form);
  var $locationNameInput = $('.gllpLocationName', $form);
  var locationText = 'Please pick your location on the map above by moving the marker OR double clicking on the map.';
  $('.gllpSearchField', $mapWrapper).on("keypress", function(e) {
    if (e.keyCode == 13) {
      $searchBtn.click();
      return false; // prevent the button click from happening
    }
  });
  $(window).on('location_changed', function(e, node) {
    var locationName = $locationNameInput.val();
    var textStr = '';
    if (locationName) {
      textStr = 'Business Location: ' + locationName;
      $locationDiv.removeClass('bg-primary').addClass('bg-success');
    } else {
      textStr = locationText;
      $locationDiv.addClass('bg-primary').removeClass('bg-success');
    }
    $locationDiv.text(textStr);
  });

};


/**
 * create isotope
 */
africaone.setUpIsotope = function($isotopeWrapper) {
  var isotopeItemSelector = '.isotope-item';

  //append grid sizer
  var $gridSizingElem = $('.grid-sizer', $isotopeWrapper);
  if ($gridSizingElem.length<=0) {
    $('<div class="grid-sizer '+$(isotopeItemSelector+':first-child', $isotopeWrapper).attr('class')+'"></div>').appendTo($isotopeWrapper);
  }

  //set up isotope
  $isotopeWrapper.isotope({
    itemSelector: isotopeItemSelector,
    masonry: {
      columnWidth: '.grid-sizer'
    },
    sortBy: 'original-order'
  });

};


/**
 * initiate isotope
 */
africaone.initiateIsotope = function($wrapper) {

  //on resize of window
  $(window).on("debouncedresize", function() {
    var viewportWidth = $(window).width();

    //check for isotope lists
    var $isotopeWrappers = $('.isotope-list', $wrapper);
    $isotopeWrappers.each( function(index, elem) {
      var $isotopeWrapper = $(elem);

      //check if data exists
      var isotopeData = {
        active: false,
        leastWidth: 0
      };
      if ($isotopeWrapper.data('isotope-data')) {
        isotopeData = $isotopeWrapper.data('isotope-data');
      } else {
        isotopeData.leastWidth = 600;
      }

      //set up isotope if width is correct and it is inactive
      if (!isotopeData.active && viewportWidth > isotopeData.leastWidth) {
        africaone.setUpIsotope($isotopeWrapper, $wrapper);
        isotopeData.active = true;
      }

      //if isotope is active, relayout or destroy it
      if (isotopeData.active) {
        if (viewportWidth > isotopeData.leastWidth) {
          $isotopeWrapper.isotope('layout');
        } else {
          $isotopeWrapper.isotope('destroy');
          isotopeData.active = false;
        }
      }

      $isotopeWrapper.data('isotope-data', isotopeData);

    });

  }).trigger( "debouncedresize" );

};


/**
 * prepare ajax calls
 */
africaone.getCookie = function (name) {
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
africaone.csrfSafeMethod = function (method) {
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
};
africaone.prepareAjaxCalls = function () {
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!africaone.csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", africaone.getCookie('csrftoken'));
      }
    }
  });
};


/**
 * initialise chosen selects
 */
africaone.initialiseBusinessListingPage = function() {

  var $rightColWrapper = $('#right-col-main-content');
  var $contentWrapper = $('.admin-dashboard-index-page-wrapper', $rightColWrapper);
  var $filtersWrapper = $('.x_panel.filters-wrapper', $contentWrapper);
  var $tilesWrapper = $('.row.tile_count', $contentWrapper);
  var $paginationWrapper = $('.pagination-wrapper', $contentWrapper);
  var $footer = $('footer');
  var $businessesListWrapper = $('.businesses-list', $contentWrapper);
  var $businessesListHeading = $('.businesses-list-heading', $contentWrapper);

  if ($contentWrapper.length <= 0) {
    return;
  }

  //manage height of business listing div
  $(window).on('debouncedresize', function() {
    setTimeout(function() {
      var viewportHeight = $rightColWrapper.height();
      var filtersHeight = $filtersWrapper.outerHeight(true);
      var tilesHeight = ($filtersWrapper.hasClass('fixed-at-top')) ? 0 : $tilesWrapper.outerHeight(true);
      var paginationHeight = $paginationWrapper.outerHeight(true);
      var footerHeight = $footer.outerHeight(true);
      var headingHeight = $businessesListHeading.outerHeight(true);
      //var businessListHeight = viewportHeight - tilesHeight - filtersHeight - paginationHeight - footerHeight - headingHeight;
      var businessListHeight = viewportHeight - filtersHeight - paginationHeight - footerHeight - headingHeight;
      $businessesListWrapper.height(businessListHeight);
    }, 400);
  }).trigger('debouncedresize');

};


/**
 * manage reviews page
 */
africaone.manageReviews = function() {

  var $rightColWrapper = $('#right-col-main-content');
  var $contentWrapper = $('.manage-reviews-page-wrapper', $rightColWrapper);
  var $contentInnerWrapper = $('.scroll-view-content', $rightColWrapper);
  var $filtersWrapper = $('.x_panel.filters-wrapper', $contentWrapper);
  var $h1 = $('h1', $contentWrapper);

};


/**
 * general functionality
 */
africaone.generalFunctionality = function() {

  //categories select
  $('select#category').select2({
    ajax: {
      url: '/manager/get_categories',
      dataType: 'json',
      delay: 250,
      data: function (params) {
        return {
          query: params.term // search term
        };
      },
      processResults: function (data, params) {
        var results = new Array();
        $.each(data.suggestions, function (index, suggestion) {
          results.push({
            id: suggestion.data,
            text: suggestion.value
          });
        });
        return {
          results: results
        };
      },
      cache: true
    },
    minimumInputLength: 2
  });

  //sticky filters
  var $rightColWrapper = $('#right-col-main-content');
  var $contentWrapper = $('.sticky-filters-page-wrapper', $rightColWrapper);
  var $contentInnerWrapper = $('.scroll-view-content', $rightColWrapper);
  var $filtersWrapper = $('.x_panel.filters-wrapper', $contentWrapper);
  var $triggerContent = $('h1', $contentWrapper);

  if ($contentWrapper.length > 0) {
    if ($contentWrapper.hasClass('dashboard-businesses-list-wrapper')) {
      $triggerContent = $('.row.tile_count', $contentWrapper);
    }
    $rightColWrapper.scroll( function() {
      var headingIsVisible = isScrolledIntoView($triggerContent);
      if (headingIsVisible) {
        $filtersWrapper.removeClass('fixed-at-top').css('width', '100%');
      } else {
        $filtersWrapper.addClass('fixed-at-top');
        $filtersWrapper.outerWidth($contentInnerWrapper.width());
      }
    });
    var isScrolledIntoView = function (elem) {
      var $elem = $(elem);
      var $window = $(window);

      var docViewTop = $window.scrollTop();
      var docViewBottom = docViewTop + $window.height();

      var elemTop = $elem.offset().top;
      var elemBottom = elemTop + $elem.height();

      return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
    };
  }

};



$(window).ready( function() {
  africaone.prepareAjaxCalls();
  africaone.initiateBusinesses();
  africaone.initialiseBusinessForm();
  africaone.initialiseBusinessListingPage();
  africaone.manageReviews();
  africaone.generalFunctionality();
});

