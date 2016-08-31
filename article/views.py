from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response
from article.models import Article, Comment
from django.http import HttpResponse
from forms import ArticleForm, CommentForm
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.utils import timezone
# Create your views here.



def articles(request):
    language = 'en-us'
    session_language = 'en-us'
    if 'lang' in request.COOKIES:
        language = request.COOKIES['lang']

    if 'lang' in request.session:
        session_language = request.session['lang']

    return render_to_response('articles.html', {'articles': Article.objects.all(), 'language': language,
                                                'session_language': session_language })

def article(request, article_id=1):
    return render_to_response('article.html', {'article': Article.objects.get(id=article_id)})

def language(request, language='en-us'):
    response = HttpResponse("setting languagae to %s" %language)
    response.set_cookie('lang', language)
    request.session['lang'] = language
    return response

def hello(request):
    name = "zukin"
    html = "<html><body>Hi %s , this seems to have worked!</body></html>" % name
    return HttpResponse(html)

def hello_template(request):
    name = "zukin"
    t = get_template('hello.html')
    html = t.render(Context({'name':name}))
    return HttpResponse(html)

def hello_template_simple(request):
    name = "zukin"
    return render_to_response('hello.html', {'name':name})


class HelloTemplate(TemplateView):

     template_name = "hello_class.html"

     def get_context_data(self, **kwargs):
         context = super(HelloTemplate, self).get_context_data(**kwargs)
         context['name'] = 'zukin'
         return context

def create(request):
    if request.POST:
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('/articles/all')
    else:
        form = ArticleForm()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render_to_response('create_article.html', args)

def like_article(request, article_id):
    if article_id:
        a = Article.objects.get(id=article_id)
        count = a.likes
        count += 1
        a.likes = count
        a.save()

    return HttpResponseRedirect('/articles/get/%s' % article_id)

def add_comment(request, article_id):
    a = Article.objects.get(id=article_id)
    if request.method == "POST":
        f = CommentForm(request.POST)
        if f.is_valid():
            c = f.save(commit=False)
            c.pub_date = timezone.now()
            c.article = a
            c.save()
            return HttpResponseRedirect('/articles/get/%s' % article_id)
    else:
        f = CommentForm()
    args = {}
    args.update(csrf(request))
    args['article'] = a
    args['form'] = f
    return render_to_response('add_comment.html', args)


