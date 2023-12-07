from django import forms


class CreateClaimForm(forms.Form):
    email = forms.EmailField()
    title = forms.CharField(max_length=200)
    content = forms.CharField(max_length=500)