jQuery(document).ready(function($) {


    // Perform AJAX login on form submit
    $('form#login').on('submit', function(e){
        $('form#login p.status').show().html(ajax_login_object.loadingmessage);
        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: ajax_login_object.ajaxurl,
            data: { 
                'action': 'ajaxlogin', //calls wp_ajax_nopriv_ajaxlogin
                'username': $('form#login #username').val(), 
                'password': $('form#login #password').val(), 
                'security': $('form#login #security').val(),
				'g-recaptcha-response': $('form#login #g-recaptcha-response').val()},
            success: function(data){
                $('form#login p.status').html(data.message);
                if (data.loggedin == true){
                    document.location.href = ajax_login_object.redirecturl;
                }
            }
        });
        e.preventDefault();
    });
	
	// Perform AJAX login on form submit
    $('form#register').on('submit', function(e){
        $('form#register p.status').show().html(ajax_login_object.loadingmessage);
        $.ajax({
			type: 'POST',
            dataType: 'json',
            url: ajax_login_object.ajaxurl,
            data: { 
                'action': 'ajax_register', //calls wp_ajax_nopriv_ajaxregister
                'username': $('form#register #username2').val(), 
                'email': $('form#register #email').val(), 
                'upassword': $('form#register #upassword').val(), 
                'security': $('form#register #security2').val(),
                'g-recaptcha-response': $('form#register #g-recaptcha-response').val() },
				
            success: function(data){
                jQuery('form#register p.status').html(data.message);
				var timer = '';
				 function flipItNow(){
					jQuery('.forgetpasswordcontainer').fadeOut();
					jQuery('.siginupcontainer').fadeOut();
					jQuery('.siginincontainer').fadeIn();
					clearTimeout(timer);
				}
				timer = setTimeout(flipItNow, 1000);
				
            }
        });
        e.preventDefault();
    });
	
	
	// Perform AJAX forget password
    $('form#lp_forget_pass_form').on('submit', function(e){
        $('form#lp_forget_pass_form p.status').show().html(ajax_login_object.loadingmessage);
        $.ajax({
			type: 'POST',
            dataType: 'json',
            url: ajax_login_object.ajaxurl,
            data: { 
                'action': 'ajax_forget_pass', //calls wp_ajax_nopriv_ajaxregister
                'email': $('form#lp_forget_pass_form #email3').val(), 
                'security': $('form#lp_forget_pass_form #security3').val() },
				
            success: function(data){
                $('form#lp_forget_pass_form p.status').html(data.message);
            }
        });
        e.preventDefault();
    });
	
	

});

