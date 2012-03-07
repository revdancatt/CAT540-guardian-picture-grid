control = {
    
    page: 1,
    
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

        //  test the API key level
        var url = 'http://content.guardianapis.com/search?page-size=1&format=json&api-key=' + $('#apiKey').val() + '&callback=?';
        $.getJSON(encodeURI(url),
            function(json) {

                utils.log(json);
                //  check to see if we have an error
                if ('response' in json && 'status' in json.response && json.response.status == 'error') {
                    $('#apiKeyCheck .control-group').addClass('error');
                    $('#apiKeyCheck .help-inline').html(json.response.message);
                    $('#apiKey').focus();
                    return false;
                }

                //  if we are here then we need to check the userTier
                if ('response' in json && 'status' in json.response && json.response.status == 'ok' && 'userTier' in json.response) {
                    if (json.response.userTier != 'partner' && json.response.userTier != 'internal') {
                        $('#apiKeyCheck .control-group').addClass('error');
                        $('#apiKeyCheck .help-inline').html('That is not a partner tier api key');
                        $('#apiKey').focus();
                        return false;
                    }
                }

                //  Now that worked we need to store the API key and start the backfilling
                $('#getApiKey').fadeOut('slow', function() {$('#backfilling').fadeIn('fast');});
                control.setApiKey();

            }
        );

    },

    setApiKey: function() {

        var url = '/api/setApiKey?apiKey=' + $('#apiKey').val();

        $.getJSON(encodeURI(url),
            function(json) {

                //  if everything went ok, then we can move on. Otherwise, ummm, something
                if ('results' in json && 'status' in json.results && json.results.status == 'ok') {
                    $('#backfilling h2').html(json.results.stories.length + '/60');
                    control.backfill();
                }

            }
        );

    },

    backfill: function() {

        utils.log('backfilling!');

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