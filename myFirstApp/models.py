from django.db import models
from django.contrib.auth.models import User

# --- Etudiant ---
class Etudiant(models.Model):
    prenom = models.CharField(max_length=255)
    nom = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)  # ajouté
    telephone = models.CharField(max_length=20, null=True, blank=True)  # changé en CharField
    adresse = models.CharField(max_length=255, blank=True)
    date_naissance = models.DateField(null=True, blank=True)  # renommé pour cohérence
    filiere = models.CharField(max_length=100, blank=True, null=True)  # ajouté

    def __str__(self):
        return f"{self.prenom} {self.nom}"


# --- Dossier utilisateur ---
class Dossier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/', default='photos/default-user.png', blank=True)
    nom = models.CharField(max_length=100, blank=True)
    prenom = models.CharField(max_length=100, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    date_naissance = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Dossier de {self.user.username}"


# --- Cours accessible à tous les utilisateurs ---
class Cours(models.Model):
    titre = models.CharField(max_length=200)
    code = models.CharField(max_length=50, blank=True, null=True)  # ajouté
    professeur = models.CharField(max_length=100, blank=True, null=True)  # ajouté
    credits = models.PositiveIntegerField(default=3)  # ajouté
    description = models.TextField(blank=True)
    date_creation = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titre
