from django.db import models
from django.contrib.auth.models import User

class Etudiant(models.Model):
    prenom = models.CharField(max_length=255)
    nom = models.CharField(max_length=255)
    telephone = models.IntegerField(null=True)
    adresse = models.CharField(max_length=255)
    date = models.DateField(null=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

# Dossier utilisateur
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

# Cours accessible à tous les utilisateurs
class Cours(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date_creation = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titre
