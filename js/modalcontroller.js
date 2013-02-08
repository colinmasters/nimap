
jQuery(function ($) {

	// Load dialog on click
	$('#navbar .addbutton').click(function (e) {
		$('#addcompany-content').modal();

		return false;
	});
});

jQuery(function ($) {

	// Load dialog on click
	$('#navbar .aboutbutton').click(function (e) {
		$('#aboutmap-content').modal({
    		autoPosition: true,
    		containerCss: {
        		'height' : '410px'
    		},
    		position: ['20%', '25%']
		});

		return false;
	});
});

