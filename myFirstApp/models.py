from django.db import models

class Etudiant(models.Model):
  prenom = models.CharField(max_length=255)
  nom = models.CharField(max_length=255)
  telephone = models.IntegerField(null=True)
  adresse = models.CharField(max_length=255)
  date = models.DateField(null=True)