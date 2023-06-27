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
from django.urls import path, include
from appone import views

from appone.views import Index, exportReport1, exportReport21, exportReport3

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Home,name='home'),
    path('perfiles/',views.escoger_perfl,name='escoger_perfil'),
    path('perfiles/<int:pf_id>',views.activo_perfil,name='act_perf'),
    path('singup/',views.Singup,name='singup'),
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
    path('villanos/',views.villanos,name='villanos'),
    path('villanos/crear',views.new_villano,name='new_villano'),
    path('villanos/<int:vil_id>/act',views.actualiza_vilano,name='villanos_act'),
    path('villanos/<int:vil_id>/eli',views.elimina_villano,name='villanos_eli'),
    path('index/',Index.as_view(), name='index'),
    path('report/', include(('report.urls', 'report'))),
    path('peliculas/',views.peliculas,name='peliculas'),
    path('peliculas/crear',views.new_pelicula,name='new_pelicula'),
    path('peliculas/<int:pel_id>/act',views.actualiza_pelicula,name='pelicula_act'),
    path('peliculas/<int:pel_id>/eli',views.elimina_pelicula,name='pelicula_eli'),
    path('series/',views.series,name='series'),
    path('series/crear',views.new_serie,name='new_serie'),
    path('series/<int:se_id>/act',views.actualiza_serie,name='serie_act'),
    path('series/<int:se_id>/eli',views.elimina_serie,name='serie_eli'),
    path('juegos/',views.juegos,name='juegos'),
    path('juegos/crear',views.new_juego,name='new_juego'),
    path('juegos/<int:jue_id>/act',views.actualiza_juego,name='juego_act'),
    path('juegos/<int:jue_id>/eli',views.elimina_juego,name='juego_eli'),
    path('organizaciones/',views.organizaciones,name='organizaciones'),
    path('organizaciones/crear',views.new_organizacion,name='new_organizacion'),
    path('organizaciones/<int:org_id>/act',views.actualiza_organizacion,name='organizacion_act'),
    path('organizaciones/<int:org_id>/eli',views.elimina_organizacion,name='organizacion_eli'),
    path('export_reporte_1/', exportReport1, name='export_reporte1'),
    path('export_reporte_2/', exportReport21, name='export_reporte2'),
    path('export_reporte_3/', exportReport3, name='export_reporte3'),
    path('sedes/',views.sedes,name='sedes'),
    path('sedes/crear',views.new_sede,name='new_sede'),
    path('sedes/<int:sed_id>/act',views.actualiza_sede,name='sede_act'),
    path('sedes/<int:sed_id>/eli',views.elimina_sede,name='sede_eli'),
    path('poderes/',views.poderes,name='poderes'),
    path('poderes/crear',views.new_poder,name='new_poder'),
    path('poderes/<int:pod_id>/act',views.actualiza_poder,name='poder_act'),
    path('poderes/<int:pod_id>/eli',views.elimina_poder,name='poder_eli'),
    path('objetos/',views.objetos,name='objetos'),
    path('objetos/crear',views.new_objeto,name='new_objeto'),
    path('objetos/<int:obj_id>/act',views.actualiza_objeto,name='objeto_act'),
    path('objetos/<int:obj_id>/eli',views.elimina_objeto,name='objeto_eli'),
    path('lista/',views.Lista_guardados,name='listguardados'),
    path('lista/<int:med_id>/cal',views.lg_calificar,name='lg_calificar'),
    path('lista/<int:med_id>/eli',views.lg_eliminar,name='lg_eli'),
    path('lista/<int:med_id>/guardar',views.lg_guardar,name='lg_guardar'),
]

