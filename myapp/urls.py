
from django.contrib import admin
from django.urls import path
from .views import article_hundler


urlpatterns = [
    path('<int:article_number>/', article_hundler, name='article'),
    path('<int:article_number>/<slug:slug_text>/', article_hundler, name='article'),
]
