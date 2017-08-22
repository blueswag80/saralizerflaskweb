"""
The flask application package.
"""

from flask import Flask
import saralizerflaskweb.views

app = Flask(__name__)
app.config.from_object('config.defaultconfig')

