from datetime import datetime
from django.shortcuts import redirect, render
from django.views import View
from .forms import CreateClaimForm

from product.models import Product

from .models import Claim

# Create your views here.

class CreateClaimView(View):
    def get(self,request,product_id):
        return render(request,"claim/create_claim.html")
    
    def post(self,request, product_id):
        form=CreateClaimForm()
        if request.method == 'POST':
            form=CreateClaimForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
                date= datetime.now()
                product=Product.objects.get(id=product_id)
                claim=Claim(username=username, content=content,product=product, date=date, title=title)
                claim.save()
                return redirect('home')
            else:
                return render(request, "claim/create_claim.html", {'form': form})
        return render(request, "claim/create_claim.html", {'form': form})
