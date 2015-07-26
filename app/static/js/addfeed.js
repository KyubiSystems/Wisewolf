// Attach a submit handler to the form
$( "#add-rss-url" ).submit(function( event ) {

	// Stop form from submitting normally
	event.preventDefault();

	// Get some values from elements on the page
	var $form = $( this ),
	    term = $form.find( "input[name='a']" ).val(),
	    url = $form.attr( "action" );

	// Send the data via AJAX post
	var posting = $.post( url, { a: term } );

	// Process results on completion
	posting.done(function( data ) {
		
		// Append AJAX response to banner text
		$( "#messagecontent" ).empty().append( data.message );
		    
		if (data.status_code == 200) {
		    // Show banner for success
		    $( "#message" ).addClass( "success" );

		} else {
		    // Show banner for error
		    $( "#message" ).addClass( "failure" );

		}

		// Fade in status banner
		$( "#message" ).fadeIn( "slow" );

		// Fade out banner on click
		$( "#message a.close-notify").click( function() {

			$( "#message" ).fadeOut( "slow" );
			$( "#message" ).deleteClass( "success failure");
			return false;

		    });


	    });

    });