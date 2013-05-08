import datetime

from flask import url_for

from ianb import db

class Post(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True)

    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    def __unicode__(self):
        return unicode(self.title)

    @property
    def type(self):
        return self.__class__.__name__

    @property
    def pretty_created_at(self):
        return self.created_at.date().strftime('%B %d, %Y')

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug'],
        'ordering': ['-created_at']
    }

class BlogPost(Post):
    body = db.StringField(required=True)

class VideoPost(Post):
    caption = db.StringField()
    embed = db.StringField(required=True)

class ImagePost(Post):
    caption = db.StringField()
    image_url = db.StringField(required=True)

class QuotePost(Post):
    body = db.StringField(required=True)
    author = db.StringField(verbose_name="Author name", max_length=255, required=True)