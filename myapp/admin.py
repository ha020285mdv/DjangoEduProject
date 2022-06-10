from django.contrib import admin
from myapp.models import Writer, Publication, Member, Author, Book
from myapp.models import Like, Comment, Article, Profile


admin.site.register(Writer)
admin.site.register(Publication)

admin.site.register(Member)
admin.site.register(Author)
admin.site.register(Book)

admin.site.register(Profile)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Like)




