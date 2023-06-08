from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from config import *

app = Flask(name)

app.config.from_object("config")
toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route
