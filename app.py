from flask import Flask


from flask import render_template
from json import load

app = Flask(__name__)
@app.route('/')
def index_site():
    return ""