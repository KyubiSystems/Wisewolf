// jQuery AJAX delete function
$.delete = function(url, data, callback, type){
 
    if ( $.isFunction(data) ){
	type = type || callback,
        callback = data,
        data = {}
    }
 
    return $.ajax({
	    url: url,
	    type: 'DELETE',
	    success: callback,
	    data: data,
	    contentType: type
	});
}

// deletePost: remove post #id from list
// TODO: AJAX delete against REST service 
function deletePost(id) {
    
    var postId = ".post-" + id;
    $( postId ).fadeOut("slow");

}