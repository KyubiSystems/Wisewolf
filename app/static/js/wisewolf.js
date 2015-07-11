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
function deletePost(id) {
    
    var url = "/post/" + id;
    $.delete( url, function(data) {

	    if (data.status_code == 200) {
		var postId = ".post-" + id;
		$( postId ).fadeOut("slow");
	    }

	});

}

// deleteFeed: remove feed #id from list
function deleteFeed(id) {

    var url = "/feed/" + id;
    $.delete( url, function(data) {
	    
	    if (data.status_code == 200) {
		var feedId = ".feed-" + id;
		$( feedId ).fadeOut("slow");
	    }
	    
	});
    
}

// deleteCategory: remove category #id from list
function deleteCategory(id) {

    var url = "/category/" + id;
    $.delete( url, function(data) {

	    if (data.status_code == 200) {
		var categoryId = ".category-" + id;
		$( categoryId ).fadeOut("slow");
	    }

	});

}

// deleteImage: remove image #id from list
function deleteImage(id) {

    var url = "/image/" + id;
    $.delete( url, function(data) {

	    if (data.status_code == 200) {
		var imageId = ".image-" + id;
		$( imageId ).fadeOut("slow");
	    }

	});

}
