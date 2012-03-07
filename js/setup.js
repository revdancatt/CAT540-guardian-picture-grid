control = {
    
    init: function() {

        $('#apiKeyCheck').submit( function() {
            control.validateApiKey();
            return false;
        });
    },

    validateApiKey: function() {

        //  check to see if there's anything there in the first place
        if ($('#apiKey').val() === '') {
            $('#apiKeyCheck .control-group').addClass('error');
            $('#apiKeyCheck .help-inline').html('You need to enter an API key');
            $('#apiKey').focus();
            return false;
        }
    }

};

utils = {
    
    log: function(msg) {
        try {
            console.log(msg);
        } catch(er) {
        }
    }
};