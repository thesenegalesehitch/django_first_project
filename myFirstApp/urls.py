from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # nécessaire pour les vues intégrées

urlpatterns = [
    # Pages principales
    path('', views.home, name='home'),
    path('myFirstApp/', views.apprenants, name='etudiants'),
    path('myFirstApp/details/<int:id>/', views.details, name='details'),

    # Authentification
    path('inscription/', views.inscription, name='inscription'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    # Pages supplémentaires (protégées)
    path('cours/', views.cours, name='cours'),
    path('contact-us/', views.contact_us, name='contact_us'),

    # Réinitialisation du mot de passe
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
]
