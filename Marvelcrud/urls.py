"""
URL configuration for Marvelcrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from appone import views

from appone.views import Index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Home,name='home'),
    path('singup/',views.Singup,name='singup'),
    path('tasks/',views.tasks,name='tasks'),
    path('tasks_completed/',views.tasks_completed,name='tasks_completed'),
    path('tasks/create',views.create_task,name='create_task'),
    path('tasks/<int:task_id>',views.task_detail,name='task_detail'),
    path('tasks/<int:task_id>/complete',views.complete_task,name='complete_task'),
    path('tasks/<int:task_id>/delete',views.delete_task,name='delete_task'),
    path('logout/',views.singout,name='logout'),
    path('singin/',views.singin,name='singin'),
    path('sub/',views.seleccionar_subscripcion,name='sub'),
    path('sub/<int:susid>',views.registrar_subscripcion,name='reg_sub'),
    path('newtdc',views.registro_tdc,name='newtdc'),
    path('civiles/',views.Civiles,name='civiles'),
    path('civiles/crear',views.new_civil,name='new_civil'),
    path('civiles/<int:civil_id>/act',views.actualiza_civil,name='civiles_act'),
    path('civiles/<int:civil_id>/eli',views.elimina_civil,name='civiles_eli'),
    path('heroes/',views.Heroes,name='heroes'),
    path('heroes/crear',views.new_heroe,name='new_heroe'),
    path('heroes/<int:heroe_id>/act',views.actualiza_heroe,name='heroes_act'),
    path('heroes/<int:heroe_id>/eli',views.elimina_heroe,name='heroes_eli'),
    path('rep1/',Index.as_view(), name='index'),
]

