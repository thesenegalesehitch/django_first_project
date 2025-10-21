from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from .models import Dossier

@receiver(post_save, sender=User)
def creer_dossier_et_groupe(sender, instance, created, **kwargs):
    if created:
        # Créer un Dossier vide avec avatar par défaut
        Dossier.objects.create(user=instance)
        
        # Attribuer un groupe par défaut
        if instance.is_superuser:
            group_name = 'admin'
        else:
            group_name = 'etudiant'
        group, _ = Group.objects.get_or_create(name=group_name)
        instance.groups.add(group)
