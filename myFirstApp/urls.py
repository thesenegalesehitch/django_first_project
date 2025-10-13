from django.urls import path
from . import views

urlpatterns = [
    path('myFirstApp/', views.apprenants, name='etudiants'),
    path('myFirstApp/details/<int:id>', views.details,name='details'),
    # path('', views.main, name='main'),
    #path('template/', views.templates, name='template'),
    path('', views.home, name='home'),
    path('inscription/', views.inscription, name='inscription'),
]
