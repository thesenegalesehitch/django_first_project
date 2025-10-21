from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Pages principales
    path('', views.home, name='home'),
    path('myFirstApp/', views.gestion_etudiants, name='etudiants'),  # renommé pour correspondre à views.py
    path('myFirstApp/details/<int:id>/', views.details_etudiant, name='details_etudiant'),

    # Authentification
    path('inscription/', views.inscription, name='inscription'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    # Pages protégées
    path('cours/', views.cours_list, name='cours'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('mon-dossier/', views.mon_dossier, name='mon_dossier'),
    path('dossier-detail/', views.dossier_detail, name='dossier_detail'),

    # Réinitialisation mot de passe
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('password_reset_display/<str:username>/', views.password_reset_display, name='password_reset_display'),
]

# Servir les fichiers médias pendant le debug
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
