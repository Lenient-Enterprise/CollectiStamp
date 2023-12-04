# company/views.py
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Company

@require_http_methods(["GET"])
def company_details(request):
    company = Company.objects.first()
    if company is not None:
        company.description = company.description.replace('\n\n', '<br>')
        return render(request, 'company/details.html', {'company': company})
    else:
        return render(request, 'company/no_data.html')
