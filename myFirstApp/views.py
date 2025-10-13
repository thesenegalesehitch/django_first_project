from django.http import HttpResponse
from django.template import loader
from .models import Etudiant
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import FormulaireInscription
from django.contrib import messages

def inscription(request):
  form=FormulaireInscription()
  
  if request.method == 'POST':
    form=FormulaireInscription(request.POST)
    if form.is_valid():
      form.save()

      user = form.cleaned_data.get('username')
      messages.success(request, 'le compte a etait créé pour '+user)

      return redirect('login')
      


  context= {
    'formulaire': form
  }
  return render(request, 'inscription.html', context)

def login(request):
  context= { }
  return render(request, 'login.html', context)


def apprenants(request):
  etudiants = Etudiant.objects.all().values()
  template = loader.get_template('etudiants.html')
  context = {
    'etudiants': etudiants,
  }
  return HttpResponse(template.render(context, request))

def details(request, id):
  etudiant = Etudiant.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
    'etudiant': etudiant,
  }
  return HttpResponse(template.render(context, request))

def home(request):
  template = loader.get_template('home.html')
  return HttpResponse(template.render())

def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def template(request):
  mesdonnees = Etudiant.objects.all().values()
  donneesfiltres = Etudiant.objects.filter(prenom='djibril').values()
  nomdonnees = Etudiant.objects.filter(prenom__startswith='I').values()
  ordonnees = Etudiant.objects.all().order_by('nom').values()
  template = loader.get_template('template.html')
  context = {
    'mesdonnees': mesdonnees,
    'donneesfiltres': donneesfiltres,
    'nomdonnees': nomdonnees,
    'ordonnees': ordonnees,
  }
  return HttpResponse(template.render(context, request))