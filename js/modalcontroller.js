
jQuery(function ($) {

	// Load dialog on click
	$('#textlink .addbutton').click(function (e) {
		$('#addcompany-content').modal();

		return false;
	});
});

jQuery(function ($) {

	// Load dialog on click
	$('#textlink .aboutbutton').click(function (e) {
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

jQuery(function ($) {

	// Load dialog on click
	$('#textlink .terms').click(function (e) {
		$('#terms-content').modal({
    		autoPosition: true,
    		containerCss: {
        		'height' : '410px'
    		},
    		position: ['20%', '25%']
		});

		return false;
	});
});

jQuery(function ($) {

	// Load dialog on click
	$('#textlink .privacy').click(function (e) {
		$('#privacy-content').modal({
    		autoPosition: true,
    		containerCss: {
        		'height' : '410px'
    		},
    		position: ['20%', '25%']
		});

		return false;
	});
});