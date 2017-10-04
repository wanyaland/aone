window.FilterListing = function(){
    jQuery('.tags-area').remove();
    jQuery('.lp-filter-pagination-ajx').remove();
    jQuery(".chosen-select").val('').trigger('chosen:updated');
    jQuery("#searchtags").prop('disabled', true).trigger('chosen:updated');
    listStyle = jQuery("#page").data('list-style');


    var inexpensive='';
    moderate = '';
    pricey = '';
    ultra = '';
    averageRate = '';
    mostRewvied = '';
    listing_openTime = '';

    inexpensive = jQuery('.currency-signs #inexpensive').find('.active').data('price');
    moderate = jQuery('.currency-signs #moderate').find('.active').data('price');
    pricey = jQuery('.currency-signs #pricey').find('.active').data('price');
    ultra = jQuery('.currency-signs #ultra').find('.active').data('price');

    averageRate = jQuery('.search-filters li#listingRate').find('.active').data('value');
    mostReviewed = jQuery('.search-filters li#listingReviewed').find('.active').data('value');
    listing_openTime = jQuery('.search-filters li#listing_openTime').find('.active').data('value');

    var tags_name = [];
    tags_name = jQuery('.tags-area input[type=checkbox]:checked').map(function(){
      return jQuery(this).val();
    }).get();
    skeyword = jQuery('input#lp_current_query').val();

    var category_id = jQuery("#searchcategory").val();
    var location_id = jQuery("#lp_search_loc").val();
    var search_tags = jQuery("#searchtags").val();

    jQuery( "body" ).prepend( '<div id="full-overlay"></div>' );
    jQuery('#full-overlay').css('height',jQuery( document ).height()+'px');

    jQuery('.lp-filter-pagination-ajx').remove();
    jQuery('#content-grids').addClass('content-loading');
    jQuery.ajax({
        type: 'GET',
        url: '/business/listing/',
        async: true,
        data: {
            'response_type': "ajax_html",
            'action': 'ajax_search_tags',
            'tag_name': search_tags,
            'category_id': category_id,
            'loc_id': location_id,
            'inexpensive':inexpensive,
            'moderate':moderate,
            'pricey':pricey,
            'ultra':ultra,
            'average_rate':averageRate,
            'most_reviewed':mostReviewed,
            'open_time':listing_openTime,
            'tag_name':tags_name,
            'list_style123': listStyle,
            'skeyword': skeyword
            },

        beforeSend: function(){
            jQuery("#listing_content").remove();
        },

        success: function(data, textStatus, jqXHR ){
            if(data.count){
                jQuery("#listing_content").remove();
                jQuery("#content-grids").append(jQuery(data.html));
                jQuery("#no_result").hide();
                jQuery("#error_result").hide();

            }
            else{
                jQuery("#no_result").show();
                jQuery("#error_result").hide();

            }
        },
        error: function(){
            jQuery("#no_result").hide();
            jQuery("#error_result").show();
        },
        complete: function(jqXHR, textStatus){
            jQuery('#full-overlay').remove();
            jQuery('#content-grids').removeClass('content-loading');
        }
    });
}
