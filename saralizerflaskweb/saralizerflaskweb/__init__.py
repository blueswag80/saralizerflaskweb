"""
The flask application package.
"""

from flask import Flask

app = Flask(__name__)
UPLOAD_FOLDER = "C:\\Users\\michael.murphy\\Documents\\Visual Studio 2017\\Projects\\saralizerflaskweb\\upload"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = '\xe8K\x0cx\x06\x8c8:\xb1n1\xd2{\x19{\xafV\xe9z\xc2\x04y<\x19'

import saralizerflaskweb.views
