from django.contrib import admin
from django.urls import path, re_path, include

from myapp.views import main, uuid, phone_regex, acricles, acricles_archive, users

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main),
    path('acricles/', acricles),
    path('acrticles/archive/', acricles_archive),
    path('users/', users),
    path('users/<int:user_number>/', users),
    path('article/', include('myapp.urls')),
    re_path(r'^(?P<uuid>[a-f\d]{4}-{1}[a-f\d]{6}/{1}$)', uuid),
    re_path(r'^(?P<phone>(?:050|066|095|099|067|068|096|097|098|063|093|073|091|092|094){1}\d{7}/{1}$)', phone_regex),
]
