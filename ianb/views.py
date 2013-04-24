from ianb import app
from flask import render_template

context = {
  'version': '0.01',
  'title': 'Ian Benedict',
  'twitter_username': 'Duelist',
  'github_username': 'Duelist',
}

@app.route('/')
def index():
    return render_template('index.html', context=context)

@app.errorhandler(404)
def error404(error):
    return render_template('404.html', context=context), 404