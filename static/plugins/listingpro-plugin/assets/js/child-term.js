jQuery(document).ready(function($){
/*	
	if($('form').is('#lp-submit-form')) {
		
			$('form#lp-submit-form div.pre-load').addClass('loader');
			 jQuery('#tags-by-cat').html(' ');
			 jQuery('#features-by-cat').html(' ');
			 jQuery(".chosen-select").prop('disabled', true).trigger('chosen:updated');
				$.ajax({
					type: 'POST',
					dataType: 'json',
					url: ajax_term_object.ajaxurl,
					data: { 
						'action': 'ajax_term', 
						'term_id': $('form#lp-submit-form #inputCategory').val(), 
						},
					success: function(data){
						if(data){						
							$('.featuresDataRow').fadeIn();
							$('form#lp-submit-form div.pre-load').removeClass('loader');
							jQuery(".chosen-select").prop('disabled', false).trigger('chosen:updated');
							jQuery.each(data.tags, function(i,v) {   						
								jQuery('#tags-by-cat')
								.append('<div class="col-md-2 col-sm-4 col-xs-6"><div class="checkbox pad-bottom-10"><input id="check_'+v+'" type="checkbox" name="tags_by_cat[]" value="'+v+'"><label for="check_'+v+'">'+v+'</label></div></div>'); 
							});
							var num = 0
							jQuery.each(data.fields, function(i,v) {   						
								jQuery('#features-by-cat')
								.append('<div class="col-md-6 col-sm-6 col-xs-12"><label for="feature_'+v+'">'+v+'</label><input id="feature_'+v+'" class="form-control" type="text" name="form_field['+num+'][1]"><input id="feature_'+v+'" class="form-control" value="'+v+'" type="hidden" name="form_field['+num+'][0]"></div>'); 
								num++;
							});
							
						}
					}
				});
	
	}
	
*/	
	
	
	
	jQuery("#inputCategory").change(function() {
		var hasfeature = jQuery(this).find('option:selected').data('doajax');

		jQuery('.lp-nested').hide();
		jQuery('#tags-by-cat').html(' ');

		if(hasfeature===1){
			 jQuery('form#lp-submit-form div.pre-load').addClass('loader');
			 jQuery('#features-by-cat').html(' ');
			 jQuery(".chosen-select").prop('disabled', true).trigger('chosen:updated');

				jQuery.ajax({
					type: 'POST',
					dataType: 'json',
					url: ajax_term_object.ajaxurl,
					data: { 
						'action': 'ajax_term', 
						'term_id': jQuery('form#lp-submit-form #inputCategory').val(), 
						},
					success: function(data){
						
						if(data){
							
							if(data.hasfeatues==true){
								jQuery('.labelforfeatures.lp-nested').show();
								jQuery('#tags-by-cat').show();
							}
							if(data.hasfields==true){
								jQuery('#features-by-cat').show();
							}
							$('form#lp-submit-form div.pre-load').removeClass('loader');
							jQuery(".chosen-select").prop('disabled', false).trigger('chosen:updated');
							
							if(data.tags != null){
								jQuery.each(data.tags, function(i,v) {   						
									jQuery('#tags-by-cat')
									.append('<div class="col-md-2 col-sm-4 col-xs-6"><div class="checkbox pad-bottom-10"><input id="check_'+v+'" type="checkbox" name="lp_form_fields_inn[lp_feature][]" value="'+i+'"><label for="check_'+v+'">'+v+'</label></div></div>'); 
								});							
								
							}
							//var num = 0;
						
								jQuery('#features-by-cat')
								.append(data.fields); 
								//num++;

							
						}
					}
				});
		}
	});

});