from django.shortcuts import render

from collecti_stamp import settings


def home(request):
    print(settings.ALLOWED_HOSTS)
    return render(request, 'base/home.html')