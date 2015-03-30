"""
Wisewolf RSS Reader
(c) 2015 Kyubi Systems: www.kyubi.co.uk
"""

# File upload handler
# Using standard Flask builtin

import os
import magic
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

UPLOAD_FOLDER = os.path.realpath('.') + '/static/uploads'
ALLOWED_EXTENSIONS = set(['xml', 'opml'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH']= 1024 * 1024 # Max 1MB upload, RequestEntityTooLarge


# Check for allowed file extensions
def allowed_file(filename):
    return '.' in filename and os.path.splitext(filename)[1] in ALLOWED_EXTENSIONS

# Define upload route
# TODO: Add mime type check for file prior to save

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', 
                                    filename=filename))
# Define upload form
# TODO: Enable drag-and-drop

    return '''
<!doctype html>
<title>Upload new File</title>
<h1>Upload new File</h1>
<form action="" method="post" enctype="multipart/form-data">
<p><input type="file" name="file">
<input type="submit" value="Upload">
</form>
'''

# Test routine, return uploaded file
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run(debug=True)
