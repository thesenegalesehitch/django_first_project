from django.contrib import admin
from .models import Etudiant

class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'adresse', 'date')
    search_fields = ('nom', 'prenom', 'adresse')
    list_filter = ('date',)
    # list_per_page = 10
    # list_max_show_all = 100
    # list_editable = ('adresse',)
    # list_display_links = ('prenom', 'nom')
    # date_hierarchy = 'date'
    # save_on_top = True
    # empty_value_display = '-empty-'
    # readonly_fields = ('date',)

    # def get_readonly_fields(self, request, obj=None):
    #     if obj is None:
    #         return self.readonly_fields
    #     return super().get_readonly_fields(request, obj)
    

# Register your models here.
admin.site.register(Etudiant, EtudiantAdmin)

