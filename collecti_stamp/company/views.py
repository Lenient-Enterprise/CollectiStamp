# company/views.py
from django.shortcuts import render
from .models import Company

def company_details(request):
    company = Company.objects.first()
    if company is not None:
        return render(request, 'company/details.html', {'company': company})
    else:
        return render(request, 'company/no_data.html')