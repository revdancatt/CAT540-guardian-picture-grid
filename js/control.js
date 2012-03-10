control = {
    
    apiUrlHash: {},
    reloadTmr: null,
    imgWidth: 460,
    imgHeight: 276,
    fontsize: '1em',
    resizeTmr: null,

    init: function() {

        this.fetchStories(60, true);
        this.reloadTmr = setInterval("control.fetchStories(10, false)", 60000);

        $(window).resize(function() {
            utils.windowResized();
        });
        utils.windowResized();

    },

    fetchStories: function(limit, firstrun) {

        var url = '/api/getLatest';

        $.getJSON(encodeURI(url),
            function(json) {

                var results = json.results.storiesList;
                if (!firstrun) {
                    results = results.reverse();
                }

                //  go thru the results
                for (var i in results) {

                    //  check to see if we already have it
                    if (!(results[i] in control.apiUrlHash)) {
                        control.apiUrlHash[results[i]] = -1;

                        var story = json.results.stories[results[i]];

                        //  The main div that's going to hold the front and back of the story 'card'
                        var d = $('<div>').addClass('container').css({'width': control.imgWidth, 'height': control.imgHeight, 'font-size': control.fontsize + 'em'});
                        var c = $('<div>').addClass('card');

                        d.mouseenter(function() {
                            control.temp = $(this);
                            $(this).find('.back').stop(true, true).fadeIn(333);
                        });
                        d.mouseleave(function() {
                            $(this).find('.back').stop(true, true).fadeOut(666);
                        });

                        d.data('apiUrl', story.apiUrl);

                        //  The front, which holds the picture
                        var front = $('<div>').addClass('face front');
                        var img = $('<img>').addClass('bigImage').attr('src', story.imgUrl);
                        img.load( function() {
                            $(this).parents('.container').fadeTo(666, 1);
                        });


                        //  Now we need the back that has the information on it
                        var back = $('<div>').addClass('face back');
                        back.append($('<h1>').html(story.sectionName));
                        back.append($('<h2>').html(story.webTitle));

                        if ('imgCaption' in story) {
                            back.append($('<div>').addClass('photocredit').append($('<p>').html('Image credit: ' + story.imgCaption)));
                        }

                        front.append(img);
                        c.append(front);
                        c.append(back);

                        var a = $('<a>').attr({'href': story.webUrl, 'target': '_blank'});
                        a.append(c);
                        d.append(a);

                        if (firstrun) {
                            $('#bigImageHolder').append(d);
                        } else {
                            $('#bigImageHolder').prepend(d);
                        }

                    }
                }

                //  trim off any more than 60 results
                while ($('div.container').length > 60) {
                    var apiUrl = $('div.container').last().data('apiUrl');
                    if (apiUrl in control.apiUrlHash) {
                        delete control.apiUrlHash[apiUrl];
                    }
                    $('div.container').last().remove();
                }

            }
        );

    }
};


utils = {
    
    log: function(msg) {
        try {
            console.log(msg);
        } catch(er) {
        }
    },

    windowResized: function() {

        //  work out the image sizes
        var fit = parseInt($('body').width()/440, 10)+1;
        control.imgWidth = parseInt($('body').width()/fit, 10);
        control.imgHeight = parseInt(276 * control.imgWidth/460, 10);

        //  work out the font size
        //  at 440px wide the biggest font size should be 1em and line-height 1.2em
        //  220px = 0.5em
        control.fontsize = ((control.imgWidth - 220)/220*0.5)+0.5;

        //  Now set them all up
        $('div.container').css({'width': control.imgWidth, 'height': control.imgHeight, 'font-size': control.fontsize + 'em'});

    }

};