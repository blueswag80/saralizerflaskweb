"""
Routes and views for the flask application.
"""

import os
import json
from datetime import datetime
from flask import render_template, request, redirect, flash, session
from saralizerflaskweb import app
from werkzeug.utils import secure_filename
from saralizerflaskweb.filelogic import SarFile, SarZipFile, remove_sar_logs, setup_upload_directory
from saralizerflaskweb.sarparser import SarParser
from saralizerflaskweb.util import get_uuid
from werkzeug.exceptions import RequestEntityTooLarge


ALLOWED_EXTENSIONS = ['gz', 'zip', 'sar']


# Utility function for file uploads.
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/home')
def home():

    if not session.get('uid'):
        session['uid'] = get_uuid()

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

        if file:
            filename = secure_filename(file.filename)
            uploadpath = os.path.join(app.config['UPLOAD_FOLDER'], session['uid'])
            fullFilePath = os.path.join(uploadpath, filename)
            sardata = []
            setup_upload_directory(uploadpath)
            file.save(fullFilePath)
            
            if not SarZipFile.check_is_zipfile(fullFilePath):
                flash('You did not upload a zip file or it is corrupt.')
                return render_template('index.html')
            
            zipfile = SarZipFile(fullFilePath)

            if zipfile.check_uncompressed_size() > app.config['MAX_ZIP_SIZE']:
                flash('The zip file you uploaded would be too large to uncompress.')
                return render_template('index.html')

            zipfile.unzip(os.path.join(uploadpath, 'outfolder'))
            for rootpath, _, files in os.walk(os.path.join(uploadpath, 'outfolder')):
                for foundfile in files:
                    sarguy = SarParser(SarFile(foundfile, rootpath))
                    temp = sarguy.analyze_sar_log()
                    temp['day'] = int(foundfile.strip('sar'))
                    sardata.append(temp)
            # sarguy = SarParser(SarFile('sar04', os.path.join(uploadpath, 'outfolder')))
            # sarinfo = sarguy.analyze_sar_log()
            # cpudata = [[cpudata['day'], cpudata['cpuinfo'][0] + cpudata['cpuinfo'][1], float(cpudata['cpuinfo'][3])] for cpudata in sardata]
            cpudatatemp = []
            # cpuddaytemps = []
            for sarlog in sorted(sardata, key=lambda log: log['day']):
                for cpu in sarlog['cpuinfo']:
                    cpudatatemp.append([cpu[0] + cpu[1], float(cpu[3]), 'Day:' + str(sarlog['day']) + ' \n' +
                                        'Time:' + cpu[0] + cpu[1] + '\n' + 'CPU Percentage:' + cpu[3]])

            # cpudatatemp.append([data['day'], data['cpuinfo'][0] + data['cpuinfo'][1], float(data['cpuinfo'][3])])
            remove_sar_logs(uploadpath)
            return render_template('graph.html', cpudata=json.dumps(cpudatatemp))


@app.errorhandler(RequestEntityTooLarge)
def handle_large_upload(error):
    flash('The zip file you uploaded would be too large to uncompress.')
    return render_template('index.html')