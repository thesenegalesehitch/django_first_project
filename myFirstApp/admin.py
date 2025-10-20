from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Dossier, Cours

# --- Admin personnalisé pour Dossier ---
class DossierAdmin(admin.ModelAdmin):
    list_display = ('user', 'nom', 'prenom', 'telephone', 'adresse', 'date_naissance')
    search_fields = ('user__username', 'nom', 'prenom', 'adresse', 'telephone')


# --- Admin personnalisé pour Cours ---
class CoursAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_creation')
    search_fields = ('titre', 'description')
    list_filter = ('date_creation',)


# --- Admin personnalisé pour les utilisateurs ---
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')


# --- Enregistrements dans l'admin ---
admin.site.unregister(User)  # Supprime la version par défaut
admin.site.register(User, CustomUserAdmin)  # Réenregistre avec la version personnalisée
admin.site.register(Dossier, DossierAdmin)
admin.site.register(Cours, CoursAdmin)
