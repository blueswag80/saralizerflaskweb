"""
Routes and views for the flask application.
"""

import os
import json
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash
from saralizerflaskweb import app
from werkzeug.utils import secure_filename
from saralizerflaskweb.filelogic import SarFile, SarZipFile
from saralizerflaskweb.sarparser import SarParser
from werkzeug.exceptions import RequestEntityTooLarge


ALLOWED_EXTENSIONS = set(['gz', 'zip', 'sar'])

#Utility function for file uploads.
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/upload', methods=["POST"])
def upload():
    """Renders the upload and handles upload logic"""
    if request.method == "POST":

        if 'file' not in request.files:
            flash('No file part received')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            if not SarZipFile.check_is_zipfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                flash('You did not upload a zip file or it is corrupt.')
                return render_template('index.html')
            
            zipfile = SarZipFile(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            if zipfile.check_Uncompressed_Size() > 95420416:
                flash('The zip file you uploaded would be too large to uncompress.')
                return render_template('index.html')

            zipfile.unzip(os.path.join(app.config['UPLOAD_FOLDER'], 'outfolder'))
            flash('All Done!')
            return render_template('index.html')
            #sarguy = SarParser(SarFile(filename, app.config['UPLOAD_FOLDER']))
            #sarinfo = sarguy.analyze_Sar_Log()
            #cpudatatemp = []
            #for item in sarinfo:
            #   cpudatatemp.append([item[0] + item[1], float(item[3])])

            #return render_template('graph.html', cpudata=json.dumps(cpudatatemp))
        
@app.errorhandler(RequestEntityTooLarge)
def handle_large_upload(error):
    flash('The zip file you uploaded would be too large to uncompress.')
    return render_template('index.html')