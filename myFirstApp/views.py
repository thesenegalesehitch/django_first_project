from django.http import HttpResponse
from django.template import loader
from .models import Etudiant
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import FormulaireInscription
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



def inscription(request):
    form = FormulaireInscription()

    if request.method == 'POST':
        form = FormulaireInscription(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Le compte a été créé pour ' + user)
            return redirect('login')

    context = {'formulaire': form}
    return render(request, 'inscription.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Nom d’utilisateur ou mot de passe incorrect')
        context = {}
        return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def apprenants(request):
    etudiants = Etudiant.objects.all().values()
    template = loader.get_template('etudiants.html')
    context = {'etudiants': etudiants}
    return HttpResponse(template.render(context, request))

def details(request, id):
    etudiant = Etudiant.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {'etudiant': etudiant}
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

def home(request):
    return render(request, 'home.html')
    template = loader.get_template('home.html')
    return HttpResponse(template.render({}, request))

@login_required(login_url='login')
def apprenants(request):
    etudiants = Etudiant.objects.all().values()
    template = loader.get_template('etudiants.html')
    context = {'etudiants': etudiants}
    return HttpResponse(template.render(context, request))


@login_required(login_url='login')
def details(request, id):
    etudiant = Etudiant.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {'etudiant': etudiant}
    return HttpResponse(template.render(context, request))


@login_required(login_url='login')
def cours(request):
    return render(request, 'cours.html')


@login_required(login_url='login')
def contact_us(request):
    return render(request, 'contact_us.html')
