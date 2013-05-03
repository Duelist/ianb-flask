import re
from unicodedata import normalize

from flask import Blueprint, request, render_template, redirect, url_for

from flask.ext.mongoengine.wtf import model_form

from ianb import app, local_settings
from ianb.models import Post, BlogPost, VideoPost, ImagePost, QuotePost
from ianb.auth import requires_auth

admin = Blueprint('admin', __name__, template_folder='templates')
punct = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

post_map = {
    "post": BlogPost,
    "video": VideoPost,
    "image": ImagePost,
    "quote": QuotePost
}

@app.route('/admin/')
@requires_auth
def list():
	posts = Post.objects.all()
	local_settings.context['posts'] = posts
	return render_template('admin/list.html', context=local_settings.context)

@app.route('/admin/new/', methods=['GET', 'POST'])
@app.route('/admin/new/<post_type>/', methods=['GET', 'POST'])
@app.route('/admin/<slug>/', methods=['GET', 'POST'])
@requires_auth
def detail(post_type=None,slug=None):
    form = None

    if (slug):
        post = Post.objects.get_or_404(slug=slug)

        if (local_settings.context['DEBUG']):
            local_settings.context['debug_msg'] = post.type

        typed_post = post.__class__ if post.__class__ != Post else BlogPost
        post_form = model_form(typed_post, exclude=('created_at', 'slug'))

        if (request.method == 'POST'):
            form = post_form(request.form, initial=post._data)
            if (form.validate()):
                form.populate_obj(post)
                post.save()
                return redirect(url_for('list'))
        else:
            form = post_form(obj=post)
    else:
        typed_post = post_map.get(post_type) if post_type else BlogPost
        post = typed_post()
        post_form = model_form(typed_post, exclude=('created_at', 'slug'))
        form = post_form(request.form)

        if (request.method == 'POST'):
            if (form.validate()):
                form.populate_obj(post)
                post.slug = slugify(post.title)
                post.save()
                return redirect(url_for('list'))

    local_settings.context['form'] = form
    return render_template('admin/detail.html', context=local_settings.context)

def slugify(phrase=None):
    slug = []
    for word in punct.split(phrase.lower()):
        word = normalize('NFKD', word).encode('ascii','ignore')
        if word:
            slug.append(word)
    return unicode('-'.join(slug))