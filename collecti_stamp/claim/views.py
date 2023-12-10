from datetime import datetime

from django.shortcuts import redirect, render
from django.views import View
from product.models import Product

from .forms import CreateClaimForm
from .models import Claim

# Create your views here.
CREATE_CLAIM_TEMPLATE = "claim/create_claim.html"
class CreateClaimView(View):
    def get(self,request,product_id):
        return render(request,CREATE_CLAIM_TEMPLATE)
    
    def post(self,request, product_id):
        form=CreateClaimForm()
        if request.method == 'POST':
            form=CreateClaimForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
                date= datetime.now()
                product=Product.objects.get(id=product_id)
                claim=Claim(email=email, content=content,product=product, date=date, title=title)
                claim.save()
                return redirect('home')
            else:
                return render(request, CREATE_CLAIM_TEMPLATE, {'form': form})
        return render(request, CREATE_CLAIM_TEMPLATE, {'form': form})
