from flask import Blueprint, request, render_template, redirect, url_for

from flask.ext.mongoengine.wtf import model_form

from ianb import app, local_settings
from ianb.models import Post, BlogPost, VideoPost, ImagePost, QuotePost
from ianb.auth import requires_auth
from ianb.utils import slugify

admin = Blueprint('admin', __name__, template_folder='templates')

post_map = {
    "post": BlogPost,
    "video": VideoPost,
    "image": ImagePost,
    "quote": QuotePost
}

@admin.route('/admin/')
@requires_auth
def list():
	posts = Post.objects.all()
	local_settings.context['posts'] = posts
	return render_template('admin/list.html', context=local_settings.context)

@admin.route('/admin/new/', methods=['GET', 'POST'])
@admin.route('/admin/new/<post_type>/', methods=['GET', 'POST'])
@admin.route('/admin/<slug>/', methods=['GET', 'POST'])
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
                return redirect(url_for('admin.list'))
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
                return redirect(url_for('admin.list'))

    local_settings.context['form'] = form
    return render_template('admin/detail.html', context=local_settings.context)

@admin.route('/admin/<slug>/preview/')
def preview(slug=None):
    post = Post.objects.get_or_404(slug=slug)
    return render_template('admin/preview.html',
                           post=post,
                           context=local_settings.context)