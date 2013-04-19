from ianb import app
from ianb.settings import *
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html', context=context)

@app.route('/blog')
def blog():
    return render_template('blog.html', context=context)

@app.errorhandler(404)
def error404(error):
    return render_template('404.html', context=context), 404