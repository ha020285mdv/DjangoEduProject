from django.http import HttpResponse
from django.shortcuts import render


def first(request):
    return render(request, 'index.html', {'title': 'Head'})


def articles(request):
    return render(request, 'articles.html', {'title': 'List of articles'})


def archive(request):
    years = [year for year in range(2000, 2023)]
    return render(request, 'archive.html', {'title': 'Archive of articles',
                                            'years': years
                                            })


def article_hundler(request, article_number, slug_text=''):
    title = 'Article #' + str(article_number) + (('/'+ slug_text) if slug_text else '')
    return render(request, 'article.html', {'title': title,
                                            'number': article_number,
                                            'slug': slug_text
                                            })


def uuid(request, uuid):
    return HttpResponse(f"uuid-like regexp: <h2>{uuid[:-1]}</h2>")


def phone_regex(request, phone):
    return HttpResponse(f"Personal account of ukrainian abonent: <h2>+38 ({phone[:3]}) {phone[3:-1]}</h2>")

