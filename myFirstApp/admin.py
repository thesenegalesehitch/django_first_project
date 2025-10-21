from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import (
    Dossier, Cours, Etudiant, Bulletin,
    Departement, Filiere, Promotion, EmploiDuTemps
)

# --- Admin personnalisé pour Etudiant ---
@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'email', 'telephone', 'filiere', 'promotion')
    search_fields = ('prenom', 'nom', 'email', 'filiere', 'promotion__nom')
    list_filter = ('filiere', 'promotion')
    ordering = ('nom', 'prenom')

# --- Admin personnalisé pour Dossier ---
@admin.register(Dossier)
class DossierAdmin(admin.ModelAdmin):
    list_display = ('user', 'nom', 'prenom', 'telephone', 'adresse', 'date_naissance')
    search_fields = ('user__username', 'nom', 'prenom', 'adresse', 'telephone')
    ordering = ('user',)

# --- Admin personnalisé pour Cours ---
@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ('titre', 'code', 'professeur', 'credits', 'date_creation')
    search_fields = ('titre', 'code', 'professeur')
    list_filter = ('date_creation',)
    ordering = ('-date_creation',)

# --- Admin personnalisé pour Bulletin ---
@admin.register(Bulletin)
class BulletinAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'matiere', 'note', 'date_creation')
    search_fields = ('etudiant__user__username', 'matiere')
    list_filter = ('date_creation', 'matiere')

# --- Admin pour Departement ---
@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'alias')
    search_fields = ('nom', 'alias')

# --- Admin pour Filiere ---
@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'alias', 'departement')
    search_fields = ('nom', 'alias', 'departement__nom')
    list_filter = ('departement',)

# --- Admin pour Promotion (anciennement Classe) ---
@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('nom', 'filiere', 'annee')
    search_fields = ('nom', 'filiere__nom')
    list_filter = ('filiere', 'annee')

# --- Admin pour Emploi du temps ---
@admin.register(EmploiDuTemps)
class EmploiDuTempsAdmin(admin.ModelAdmin):
    list_display = ('promotion', 'jour', 'cours', 'heure_debut', 'heure_fin', 'professeur')
    search_fields = ('promotion__nom', 'cours__titre', 'professeur')
    list_filter = ('promotion', 'jour')

# --- Admin personnalisé pour les utilisateurs Django ---
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

# --- Réenregistrement de l'utilisateur ---
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
