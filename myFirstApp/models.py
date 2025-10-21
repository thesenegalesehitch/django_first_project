from django.db import models
from django.contrib.auth.models import User

# --- Departement ---
class Departement(models.Model):
    nom = models.CharField(max_length=100)
    alias = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.nom} ({self.alias})"


# --- Filiere ---
class Filiere(models.Model):
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    alias = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.nom} ({self.alias})"


# --- Promotion (anciennement Classe) ---
class Promotion(models.Model):
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    nom = models.CharField(max_length=50)  # Exemple: EMA2025, DBE2025
    annee = models.PositiveIntegerField()  # Facultatif : année académique

    def __str__(self):
        return f"{self.nom} - {self.filiere.nom}"


# --- Etudiant ---
class Etudiant(models.Model):
    prenom = models.CharField(max_length=255)
    nom = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    filiere = models.CharField(max_length=100, blank=True, null=True)
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)

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
    code = models.CharField(max_length=50, blank=True, null=True)
    professeur = models.CharField(max_length=100, blank=True, null=True)
    credits = models.PositiveIntegerField(default=3)
    description = models.TextField(blank=True)
    date_creation = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titre


# --- Bulletin ---
class Bulletin(models.Model):
    etudiant = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name="bulletins")
    matiere = models.CharField(max_length=200)
    note = models.DecimalField(max_digits=5, decimal_places=2)
    commentaire = models.TextField(blank=True)
    date_creation = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.matiere} - {self.etudiant.user.username}"


# --- Emploi du temps ---
class EmploiDuTemps(models.Model):
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, null=True, blank=True)
    jour = models.CharField(max_length=10, choices=[
        ('Lundi','Lundi'), ('Mardi','Mardi'), ('Mercredi','Mercredi'),
        ('Jeudi','Jeudi'), ('Vendredi','Vendredi'), ('Samedi','Samedi')
    ])
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    professeur = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.promotion.nom} - {self.jour} - {self.cours.titre}"
