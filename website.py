from flask import render_template, redirect
import json

db = None

def index_page(info_text = ''):
    return render_template('index.html', \
                           info_text = info_text)

