import json
import requests
import config
import pandas as pd
from flask import Flask, render_template, url_for
import requests
from flask import *
from SPARQLWrapper import SPARQLWrapper
import pickle
import re





from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def postnum():
    return render_template('hinan.html')
    

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost') 
