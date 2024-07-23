from django import forms
from . models import Articles
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . models import User



class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ("Article_links",)
        
        

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email', 'password1', 'password2']
        



class SurveyyForm(forms.Form):
    gender = [("Male","Male"),("Female","Female")]
    FirstName = forms.CharField(label="FirstName",max_length=255)
    LastName = forms.CharField(label="LastName",max_length=255)
    Gender = forms.ChoiceField(choices=gender)
    Email = forms.EmailField()
    Phone = forms.CharField(max_length=11)
    Address = forms.CharField(max_length=255)
    bio =   forms.CharField(widget=forms.Textarea)

    
    
    
    
    
