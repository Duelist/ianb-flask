import re
from unicodedata import normalize

punct = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

def slugify(phrase=None):
    slug = []
    for word in punct.split(phrase.lower()):
        word = normalize('NFKD', word).encode('ascii','ignore')
        if word:
            slug.append(word)
    return unicode('-'.join(slug))