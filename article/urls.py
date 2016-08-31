from django.conf.urls import url, include
from article.views import article
from article.views import articles
from article.views import language
from views import create

urlpatterns = [
    url(r'^all/$', articles),
    url(r'^get/(?P<article_id>\d+)/$', article),
    url(r'^language/(?P<language>[a-z\-]+)/$', language),
    url(r'^create/$', create),

]