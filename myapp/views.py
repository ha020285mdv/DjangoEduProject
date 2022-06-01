from django.http import HttpResponse


def main(request):
    return HttpResponse("My first DJANGO view")


def acricles(request):
    return HttpResponse("This is the articles store")


def acricles_archive(request):
    return HttpResponse("This is the articles archive")


def users(request, user_number=None):
    return HttpResponse(f"User ID:<h2>{user_number}</h2>" if user_number else "Users list")


def article_hundler(request, article_number, slug_text=''):
    response = f"Article #: <h2>{article_number}</h2>"
    if slug_text:
        if slug_text == 'archive':
            response += ' archived version'
        else:
            response += f"has name <h2>{slug_text}</h2"

    return HttpResponse(response)


def uuid(request, uuid):
    return HttpResponse(f"uuid-like regexp: <h2>{uuid[:-1]}</h2>")


def phone_regex(request, phone):
    return HttpResponse(f"Personal account of ukrainian abonent: <h2>+38 ({phone[:3]}) {phone[3:-1]}</h2>")
