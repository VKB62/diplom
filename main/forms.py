from django import forms


class UserForm(forms.Form):
    email = forms.EmailField()
    passw = forms.CharField(max_length=100)



