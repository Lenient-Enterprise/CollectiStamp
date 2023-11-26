from django.shortcuts import render

from collecti_stamp import settings


def home(request):
    print(settings.BASE_URL)

    return render(request, 'base/home.html')