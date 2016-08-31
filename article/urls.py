from django.conf.urls import url, include
from article.views import article
from article.views import articles
from article.views import language
from views import create, like_article, add_comment

urlpatterns = [
    url(r'^all/$', articles),
    url(r'^get/(?P<article_id>\d+)/$', article),
    url(r'^language/(?P<language>[a-z\-]+)/$', language),
    url(r'^create/$', create),
    url(r'^like/(?P<article_id>\d+)/$', like_article),
    url(r'^add_comment/(?P<article_id>\d+)/$', add_comment)

]