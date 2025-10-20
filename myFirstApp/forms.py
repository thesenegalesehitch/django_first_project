# myFirstApp/forms.py
# Formulaire d'inscription basé sur UserCreationForm
# On ajoute des widgets pour avoir des placeholders et la classe bootstrap 'form-control'
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Dossier


class FormulaireInscription(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email...'
        })
    )

    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Nom d'utilisateur..."
        })
    )

    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe...'
        })
    )

    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmer mot de passe...'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # Optionnel : nettoyer l'email pour éviter doublons si tu veux
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Un compte avec cet e-mail existe déjà.")
        return email

class DossierForm(forms.ModelForm):
    class Meta:
        model = Dossier
        fields = ['photo', 'nom', 'prenom', 'telephone', 'adresse', 'date_naissance']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
