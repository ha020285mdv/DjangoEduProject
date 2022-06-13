

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

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

    #все что было возможно делал через shell - здесь сохранил текст комманд

    # 1. Получить 5 последних написанных комментариев (именно текст)
    content['task1'] = Comment.objects.order_by('-date')[:5]

    # 2. Создать 5 комментариев с разным текстом, Хотя бы один должен начинаться со слова "Start",
    #    хоть один в середине должен иметь слово "Middle", хоть один должен заканчиваться словом "Finish".

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

    # 3. Переписать сейв комментария так, что бы при создании дата менялась бы на год назад (если
    # сегодня 20 декабря 2021, должна выставляться 20 декабря 2020), изменение комментариев не затрагивать.
    #  ==== implemented in Models.py ====
    content['task3'] = 'done'

    # 4. Изменить комментарии со словами "Start", "Middle", "Finish"

    # Comment.objects.filter(comment__istartswith='start').update(comment='START')
    # Comment.objects.filter(comment__icontains='middle').update(comment='MIDDLE')
    # Comment.objects.filter(comment__iendswith='finish').update(comment='FINISH')
    content['task4'] = 'done'

    # 5. Удалить все комментарии у которых в тексте есть буква "k", но не удалять если есть буква "с".
    # Comment.objects.filter(comment__icontains='k').exclude(comment__icontains='c').delete()
    content['task5'] = 'done'

    # 6. Получить первые 2 комментария по дате создания к статье у которой имя автора последнее по алфавиту.
    content['task6'] = Comment.objects.filter(content_type_id=15).order_by('date', '-article__author')[:2]
    # content_type_id=15 - to select the only comments for articles

    return render(request, 'homework4.html', content)
