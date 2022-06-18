from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from myapp.forms import CheckRequirementsForm, AuthForm, RegisterForm, ChangePasswordForm, FindCommentsForm
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
            name = form.cleaned_data['name']
            content = {'name': name, 'title': "Congratulations!"}
            return render(request, 'form_answer.html', content)
    else:
        # we fill the name_fild of form by name/username of logged user
        initial = {'name': (request.user.first_name or request.user.username) if request.user.is_authenticated else ''}
        form = CheckRequirementsForm(initial=initial)
    content = {'title': 'Check if you fit', 'form': form}

    return render(request, 'requirements_form.html', content)


def user_login(request):
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return HttpResponseRedirect('/')
    else:
        form = AuthForm()

    return render(request, 'login.html', {'title': 'Authentication', 'form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            first_name=form.cleaned_data['first_name'],
                                            last_name=form.cleaned_data['last_name'],
                                            email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password'])
            login(request, user)    # in the same time we authorize a new user, for convenience
            return HttpResponseRedirect('/')
    else:
        form = RegisterForm()
    return render(request, 'login.html', {'title': 'Registration', 'form': form})


@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                login(request, user)    # log in with new user data
                return HttpResponseRedirect('/')
    else:
        form = ChangePasswordForm()

    return render(request, 'change_password.html', {'title': 'Change password', 'form': form})


def find_comments_form_view(request):
    form = FindCommentsForm(request.GET)
    comments = {}
    limit = 25

    if request.GET:
        text_to_find = request.GET.get('text_to_find', '')
        comments = Comment.objects.filter(comment__icontains=text_to_find).order_by('-date')

        user = request.user.username if request.GET.get('in_own', False) else False
        if user:
            comments = comments.filter(author__login=user)

        comments = comments[:limit]

    content = {'title': 'Searching comments', 'form': form, 'comments': comments}
    return render(request, 'find_comment.html', content)
