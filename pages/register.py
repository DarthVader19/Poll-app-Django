from django.forms import ModelForm

from .models import User

class CreateUser(ModelForm):
    class Meta:
        model=User
        fields=['name','email','password']