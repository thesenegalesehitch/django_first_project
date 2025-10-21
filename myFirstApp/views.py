from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Etudiant, Dossier, Cours
from .forms import FormulaireInscription, DossierForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail

# --- Authentification ---
def inscription(request):
    if request.method == 'POST':
        formulaire = FormulaireInscription(request.POST)
        if formulaire.is_valid():
            # Créer l'utilisateur
            user = formulaire.save()
            
            # Connexion automatique du nouvel utilisateur
            login(request, user)
            
            username = formulaire.cleaned_data.get('username')
            messages.success(request, f'Bienvenue {username} ! Votre compte a été créé et vous êtes connecté.')
            return redirect('home')  # redirection sécurisée vers home
        else:
            messages.error(request, "Une erreur est survenue. Veuillez vérifier le formulaire.")
    else:
        formulaire = FormulaireInscription()

    return render(request, 'inscription.html', {'formulaire': formulaire})

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Nom d’utilisateur ou mot de passe incorrect.')

    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('home')


# --- Pages principales ---
@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def apprenants(request):
    etudiants = Etudiant.objects.all()
    return render(request, 'etudiants.html', {'etudiants': etudiants})


@login_required
def details(request, id):
    etudiant = get_object_or_404(Etudiant, id=id)
    return render(request, 'details.html', {'etudiant': etudiant})


@login_required
def contact_us(request):
    return render(request, 'contact_us.html')


# --- Gestion du dossier utilisateur ---
@login_required
def mon_dossier(request):
    dossier, created = Dossier.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Suppression de la photo si bouton "delete_photo"
        if 'delete_photo' in request.POST:
            dossier.photo.delete(save=True)
            messages.success(request, 'Photo supprimée avec succès.')
            return redirect('mon_dossier')

        form = DossierForm(request.POST, request.FILES, instance=dossier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre dossier a été mis à jour avec succès.')
            return redirect('mon_dossier')
        else:
            messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')
    else:
        form = DossierForm(instance=dossier)

    return render(request, 'mon_dossier.html', {'form': form, 'dossier': dossier})


@login_required
def dossier_detail(request):
    dossier = get_object_or_404(Dossier, user=request.user)
    return render(request, 'dossier_detail.html', {'dossier': dossier})


# --- Gestion des cours ---
@login_required
def cours_list(request):
    cours_list = Cours.objects.all().order_by('-date_creation')
    return render(request, 'cours_list.html', {'cours_list': cours_list})

def password_reset_display(request, username):
    user = User.objects.get(username=username)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_link = request.build_absolute_uri(f'/reset/{uid}/{token}/')
    return render(request, 'password_reset_display.html', {'reset_link': reset_link})

def contact_us(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Exemple d’envoi d’email (à adapter)
        send_mail(
            subject=f"[Contact ISEP] {subject}",
            message=f"De : {name} <{email}>\n\n{message}",
            from_email="webmaster@isepdiamniadio.com",
            recipient_list=["contact@isepdiamniadio.com"],
            fail_silently=False,
        )

        messages.success(request, "Votre message a été envoyé avec succès !")
        return redirect('contact_us')

    return render(request, "contact.html")