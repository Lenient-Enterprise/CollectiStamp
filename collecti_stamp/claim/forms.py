from django import forms


class CreateClaimForm(forms.Form):
    username = forms.CharField(max_length=100)
    title = forms.CharField(max_length=200)
    content = forms.CharField(max_length=500)