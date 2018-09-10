
(function (jQuery) {
    "use strict";


    /*==================================================================
    [ Focus input ]*/
    jQuery('.input100').each(function(){
        jQuery(this).on('blur', function(){
            if(jQuery(this).val().trim() != "") {
                jQuery(this).addClass('has-val');
            }
            else {
                jQuery(this).removeClass('has-val');
            }
        })    
    })
  
  
    /*==================================================================
    [ Validate ]*/
    var input = jQuery('.validate-input .input100');

    jQuery('.validate-form').on('submit',function(){
        var check = true;

        for(var i=0; i<input.length; i++) {
            if(validate(input[i]) == false){
                showValidate(input[i]);
                check=false;
            }
        }

        return check;
    });


    jQuery('.validate-form .input100').each(function(){
        jQuery(this).focus(function(){
           hideValidate(this);
        });
    });

    function validate (input) {
        if(jQuery(input).attr('type') == 'email' || jQuery(input).attr('name') == 'email') {
            if(jQuery(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        }
        else {
            if(jQuery(input).val().trim() == ''){
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = jQuery(input).parent();

        jQuery(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = jQuery(input).parent();

        jQuery(thisAlert).removeClass('alert-validate');
    }
    
    
})(jQuery);