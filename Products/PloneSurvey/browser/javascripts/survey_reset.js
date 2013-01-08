(function($) {
    $(document).ready(function(){
        jq('#survey_reset_form').submit(function() {
        	if (confirm("Are you sure you want to reset the survey?")) {
                return true;
            } else {
            	return false;
            };
	    });
	});
})(jQuery);
