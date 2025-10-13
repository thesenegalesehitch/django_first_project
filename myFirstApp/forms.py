# your_app/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User # Assuming you have a custom user model



class FormulaireInscription(UserCreationForm):
    class Meta(UserCreationForm.Meta):
      model = User 
      fields = ('username', 'email', 'first_name', 'last_name')
        # Add any additional fields you want to include in the form
class FormulaireInscription(UserCreationForm):
    class Meta():
        model = User 
        fields = ('username', 'email', 'password1', 'password2')