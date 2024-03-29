from django.contrib import admin
from django.urls import path, re_path, include

from myapp.views import uuid, phone_regex, first, articles, archive, find_comments_form_view
from myapp.views import homework4, check_requirements_form_view
from myapp.views import user_login, user_logout, user_register, change_password


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', first, name='main_page'),
    path('articles/', articles, name='articles'),
    path('articles/archive/', archive, name='archive'),
    path('article/', include('myapp.urls')),
    re_path(r'^(?P<uuid>[a-f\d]{4}-{1}[a-f\d]{6}/{1}$)', uuid),
    re_path(r'^(?P<phone>(?:050|066|095|099|067|068|096|097|098|063|093|073|091|092|094){1}\d{7}/{1}$)', phone_regex),
    path('homework4', homework4, name='hw4'),
    path('check_requirements', check_requirements_form_view, name='requirements_form'),
    path('find_comments', find_comments_form_view, name='find_comments'),

    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('register', user_register, name='register'),
    path('change_password', change_password, name='pass_chng'),
]
