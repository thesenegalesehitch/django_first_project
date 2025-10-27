from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .models import Etudiant, Dossier, Cours, Bulletin, Promotion, EmploiDuTemps
from .forms import FormulaireInscription, DossierForm

# --------------------------
# Vérifications de groupes
# --------------------------
def est_admin(user):
    return user.groups.filter(name='admin').exists()

def est_etudiant(user):
    return user.groups.filter(name='etudiant').exists()


# --------------------------
# Authentification
# --------------------------
def inscription(request):
    if request.method == 'POST':
        formulaire = FormulaireInscription(request.POST)
        if formulaire.is_valid():
            user = formulaire.save()
            group, created = Group.objects.get_or_create(name='etudiant')
            user.groups.add(group)
            Dossier.objects.get_or_create(user=user)
            login(request, user)
            username = formulaire.cleaned_data.get('username')
            messages.success(request, f'Bienvenue {username} ! Votre compte a été créé et vous êtes connecté.')
            return redirect('home')
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


# --------------------------
# Pages principales
# --------------------------
@login_required
def home(request):
    return render(request, 'home.html')


@login_required
@user_passes_test(est_admin)
def gestion_etudiants(request):
    etudiants = Etudiant.objects.all()
    return render(request, 'etudiants.html', {'etudiants': etudiants})


@login_required
def details_etudiant(request, id):
    etudiant = get_object_or_404(Etudiant, id=id)
    bulletins = Bulletin.objects.filter(etudiant__user=etudiant.user)
    return render(request, 'details.html', {'etudiant': etudiant, 'bulletins': bulletins})


@login_required
def contact_us(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        send_mail(
            subject=f"[Contact ISEP] {subject}",
            message=f"De : {name} <{email}>\n\n{message}",
            from_email="webmaster@isepdiamniadio.com",
            recipient_list=["contact@isepdiamniadio.com"],
            fail_silently=False,
        )
        messages.success(request, "Votre message a été envoyé avec succès !")
        return redirect('contact_us')

    return render(request, "contact_us.html")



@login_required
def dossier_detail(request):
    dossier = get_object_or_404(Dossier, user=request.user)
    bulletins = Bulletin.objects.filter(etudiant=dossier)
    return render(request, 'dossier_detail.html', {'dossier': dossier, 'bulletins': bulletins})


# --------------------------
# Gestion des cours
# --------------------------
@login_required
def cours_list(request):
    cours_list = Cours.objects.all().order_by('-date_creation')
    return render(request, 'cours_list.html', {'cours_list': cours_list})


# --------------------------
# Gestion des bulletins (Admin uniquement)
# --------------------------
@login_required
@user_passes_test(est_admin)
def ajouter_bulletin(request, etudiant_id):
    etudiant = get_object_or_404(Dossier, id=etudiant_id)
    if request.method == 'POST':
        matiere = request.POST.get('matiere')
        note = request.POST.get('note')
        commentaire = request.POST.get('commentaire')
        Bulletin.objects.create(
            etudiant=etudiant,
            matiere=matiere,
            note=note,
            commentaire=commentaire
        )
        messages.success(request, f"Bulletin ajouté pour {etudiant.user.username}")
        return redirect('details_etudiant', id=etudiant.id)
    return render(request, 'ajouter_bulletin.html', {'etudiant': etudiant})


# --------------------------
# Gestion des plannings
# --------------------------
@login_required
def mon_planning(request):
    try:
        etudiant = Etudiant.objects.get(user=request.user)
        if not etudiant.promotion:
            messages.warning(request, "Vous n'avez pas encore de promotion assignée.")
            planning = []
        else:
            planning = EmploiDuTemps.objects.filter(promotion=etudiant.promotion).order_by('jour', 'heure_debut')
    except Etudiant.DoesNotExist:
        messages.error(request, "Profil étudiant non trouvé.")
        planning = []

    return render(request, 'mon_planning.html', {'planning': planning})


@login_required
@user_passes_test(est_admin)
def gerer_planning(request, promotion_id):
    promotion = get_object_or_404(Promotion, id=promotion_id)
    emploi = EmploiDuTemps.objects.filter(promotion=promotion).order_by('jour', 'heure_debut')

    if request.method == 'POST':
        jour = request.POST.get('jour')
        heure_debut = request.POST.get('heure_debut')
        heure_fin = request.POST.get('heure_fin')
        cours_id = request.POST.get('cours')
        cours = get_object_or_404(Cours, id=cours_id)
        professeur = request.POST.get('professeur', '')

        EmploiDuTemps.objects.create(
            promotion=promotion,
            jour=jour,
            heure_debut=heure_debut,
            heure_fin=heure_fin,
            cours=cours,
            professeur=professeur
        )
        messages.success(request, f"Cours ajouté au planning de {promotion.nom}")
        return redirect('gerer_planning', promotion_id=promotion.id)

    return render(request, 'gerer_planning.html', {'promotion': promotion, 'emploi': emploi})


# --------------------------
# Réinitialisation mot de passe
# --------------------------
def password_reset_display(request, username):
    user = User.objects.get(username=username)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_link = request.build_absolute_uri(f'/reset/{uid}/{token}/')
    return render(request, 'password_reset_display.html', {'reset_link': reset_link})

@login_required
def mon_dossier(request):
    # Récupère ou crée le dossier pour l'utilisateur
    dossier, created = Dossier.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Suppression de la photo si demandé
        if 'delete_photo' in request.POST and dossier.photo:
            dossier.photo.delete(save=True)
            messages.success(request, 'Photo supprimée avec succès.')
            return redirect('mon_dossier')

        # Mise à jour du dossier
        form = DossierForm(request.POST, request.FILES, instance=dossier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre dossier a été mis à jour avec succès.')
            return redirect('mon_dossier')
        else:
            messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')
    else:
        form = DossierForm(instance=dossier)

    # Récupérer les bulletins uniquement si l'utilisateur est un étudiant
    bulletins = Bulletin.objects.filter(etudiant__user=request.user) if est_etudiant(request.user) else None

    return render(request, 'mon_dossier.html', {
        'form': form,
        'dossier': dossier,
        'bulletins': bulletins
    })