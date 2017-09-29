jQuery('#lp-submit-form').submit(function(e){
	var $this = jQuery(this);
	
	$this.find('.preview-section .fa-angle-right').removeClass('fa-angle-right');
	$this.find('.preview-section .fa').addClass('fa-spinner fa-spin');
	var fd = new FormData(this);
	jQuery("#listingsubmitBTN").prop('disabled',true);
	fd.append('action', 'listingpro_submit_listing_ajax');
	jQuery.ajax({
		type: 'POST',
		url: ajax_listingpro_submit_object.ajaxurl,
		data:fd,
		contentType: false,
		processData: false,
		
		success: function(res){
			
			var resp = jQuery.parseJSON(res);
			if(resp.response==="fail"){
				jQuery("#listingsubmitBTN").prop('disabled',false);
				jQuery.each(resp.status, function (k, v) {
					
					if(k==="postTitle"){
						jQuery("input:text[name='postTitle']").addClass('error-msg');	
					}
					else if(k==="gAddress"){
						jQuery("input:text[name='gAddress']").addClass('error-msg');
					}
					else if(k==="category"){
						jQuery("#inputCategory_chosen").find('a.chosen-single').addClass('error-msg');
						jQuery("#inputCategory").next('.select2-container').find('.selection').find('.select2-selection--single').addClass('error-msg');
					}
					else if(k==="location"){
						jQuery("#inputCity_chosen").find('a.chosen-single').addClass('error-msg');
						jQuery("#inputCity").next('.select2-container').find('.selection').find('.select2-selection--single').addClass('error-msg');
					}
					else if(k==="postContent"){
						jQuery("textarea[name='postContent']").addClass('error-msg');
					}
					else if(k==="email"){
						jQuery("input#inputEmail").addClass('error-msg');
					}
					
				});
				var errorrmsg = jQuery("input[name='errorrmsg']").val();
				$this.find('.preview-section .fa-spinner').removeClass('fa-spinner fa-spin');
				$this.find('.preview-section .fa').addClass('fa-times');
				$this.find('.preview-section').find('.error_box').text(errorrmsg).show();
			}
			else if(resp.response==="failure"){
				jQuery("input#inputEmail").addClass('error-msg');
				jQuery("input#inputEmail").after(resp.status);
				$this.find('.preview-section .fa-spinner').removeClass('fa-spinner fa-spin');
				$this.find('.preview-section .fa').addClass('fa-angle-right');
			}
			else if(resp.response==="success"){
				$this.find('.preview-section .fa-spinner').removeClass('fa-times');
				$this.find('.preview-section .fa-spinner').removeClass('fa-spinner fa-spin');				
				$this.find('.preview-section .fa').addClass('fa-check');
				var redURL = resp.status;
				function redirectPageNow(){
						window.location.href= redURL;
				}
				setTimeout(redirectPageNow, 1000);
				 
			}
			
			
		},
		error: function(request, error){
			alert(error);
		}
	});
	 
	e.preventDefault();
	
 }); 
  