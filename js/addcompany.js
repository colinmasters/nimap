
jQuery(function ($) {

	// Load dialog on click
	$('#navbar .addbutton').click(function (e) {
		$('#addcompany-content').modal();

		return false;
	});
});