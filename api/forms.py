from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
    # username = forms.CharField(label="Username", max_length=20)
    # password = forms.CharField(label="Password")
    
class ClassifyImageForm(forms.Form):
    image = forms.ImageField()