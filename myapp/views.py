from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from myapp.forms import CheckRequirementsForm
from myapp.models import Comment, Profile, Article


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


def homework4(request):
    content = {'title': 'Homework #4'}
    content['task1'] = Comment.objects.order_by('-date')[:5]
    # comment = Comment(comment='Comment to test', author_id='4', content_type_id='15', object_id='2')
    # comment.save()
    # objs = Comment.objects.bulk_create([
    #     Comment(comment='Start testing', author_id='1', content_type_id='14', object_id='2', date=timezone.now()),
    #     Comment(comment='With middle text', author_id='3', content_type_id='15', object_id='1', date=timezone.now()),
    #     Comment(comment='It is finish', author_id='2', content_type_id='15', object_id='1', date=timezone.now()),
    #     Comment(comment='Brilliant work!', author_id='1', content_type_id='14', object_id='2', date=timezone.now()),
    #     Comment(comment='I like it!', author_id='3', content_type_id='14', object_id='3', date=timezone.now()),
    #     ])
    content['task2'] = 'done'
    content['task3'] = 'done'
    # Comment.objects.filter(comment__istartswith='start').update(comment='START')
    # Comment.objects.filter(comment__icontains='middle').update(comment='MIDDLE')
    # Comment.objects.filter(comment__iendswith='finish').update(comment='FINISH')
    content['task4'] = 'done'
    # Comment.objects.filter(comment__icontains='k').exclude(comment__icontains='c').delete()
    content['task5'] = 'done'
    article_model_id = ContentType.objects.get(model='article').id  # to find the articles model id in generic_relation
    content['task6'] = Comment.objects.filter(content_type_id=article_model_id).order_by('date', '-article__author')[:2]

    return render(request, 'homework4.html', content)


def check_requirements_form_view(request):
    if request.method == 'POST':
        form = CheckRequirementsForm(request.POST)
        if form.is_valid():
            name = request.POST['name']
            sex = request.POST['sex']
            age = int(request.POST['age'])
            level = request.POST['english_level']

            is_fit = (sex=='m' and age>=20 and level in ['C1', 'C2']) or \
                     (sex=='f' and age>=22 and level in ['B2', 'C1', 'C2'])
            content = {'name': name, 'fit': is_fit, 'title': "Congratulations!" if is_fit else "Don't worry!"}

            return render(request, 'form_answer.html', content)
    else:
        form = CheckRequirementsForm()
    content = {'title': 'Check if you fit', 'form': form}

    return render(request, 'requirements_form.html', content)




"""Практика / Домашка:
Пишем страницу логина и логаута руками, проверяем, что всё работает.

Написать страницу для регистрации. (не забываем про set_password)
Следующая страница должна открываться только залогиненым пользователям
Пишем страницу для смены пароля. (Запрашиваем текущий пароль 2 раза, и проверяем через check_password)
Написать страницу с гет формой, для поиска по тексту ваших комментариев, отобразить все найденные частичные совпадение, без учёта регистра.
Добавить к поиску по комментариям галочку, что бы при нажатой галочке показывало только твои комментарии
"""

