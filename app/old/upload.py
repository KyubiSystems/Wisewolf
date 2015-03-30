"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

import os.path
from flask import Flask, redirect, request, url_for
from flask.ext.uploads import delete, init, save, upload

app.config['DEFAULT_FILE_STORAGE'] = 'filesystem'
app.config['UPLOADS_FOLDER'] = os.path.realpath('.') + '/static/uploads'
app.config['FILE_SYSTEM_STORAGE_FILE_VIEW'] = 'static'

@app.route('/upload', methods=['GET','POST'])
def upload():
    """Upload a new file"""
    if request.method == 'POST':
        print 'saving'
        save(request.files['upload'])
        return redirect(url_for('index'))

    return (
        render_template('upload.html')
        )

@app.route('/clear/<int:id>', method=['POST'])
def clear(id):
    """Delete an uploaded file"""
    upload = Upload.query.get_or_404(id)
    delete(upload)
    return redirect(url_for('index'))
