from flask import Blueprint, render_template

from mongoengine.queryset import Q

from ianb import app, local_settings
from ianb.models import Post

blog = Blueprint('blog', __name__, template_folder='templates')

@blog.route('/')
def list():
    posts = Post.objects.filter(Q(draft__exists=False) | Q(draft=False))
    return render_template('blog/list.html',
                           posts=posts,
                           context=local_settings.context)

@blog.route('/<slug>/')
def detail(slug=None):
    post = Post.objects.get_or_404(slug=slug)
    return render_template('blog/detail.html',
                           post=post,
                           context=local_settings.context)

@app.errorhandler(404)
def error404(error):
    return render_template('404.html', context=local_settings.context), 404