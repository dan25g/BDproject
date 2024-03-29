from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages
from django.db import IntegrityError
from .forms import *
from .models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
#from django.contrib.auth.models import Personaje
from psycopg2 import *
from report.report import report
# Create your views here.

class Index(TemplateView):
            template_name = "index.html"

def exportReport1(request):
    conexion= connect(host="localhost",database="marveldb",user="postgres",password="12345679")
    cur=conexion.cursor()

    cur.execute("select h.nombre_superheroe as nombre, p2.tipo "+
                " from infopersonajes.poder p, infopersonajes.personaje_poder a, infopersonajes.heroe h, infopersonajes.personaje p2, infopersonajes.historico_personaje o "+
                " where (h.personaje_id=p2.personaje_id) and ((h.personaje_id = a.fk_pers_pod)) and (p.podid = a.fk_pod_pers) and (p.ponaturaleza = 'Artificial') and (h.personaje_id=o.fk_pers_org) and (o.lider = true) "+
                " UNION ALL "+ 
                " select v.nombre_supervillano as nombre, p2.tipo "+
                " from infopersonajes.poder p, infopersonajes.personaje_poder a, infopersonajes.villano v, infopersonajes.personaje p2, infopersonajes.historico_personaje o "+
                " where (v.personaje_id=p2.personaje_id) and (v.personaje_id = a.fk_pers_pod) and (p.podid = a.fk_pod_pers) and (p.ponaturaleza = 'Artificial') and (v.personaje_id=o.fk_pers_org) and (o.lider = true);")

    personajes_list= []
    for nombre, tipo in cur.fetchall():# data={nombre:tipo}
        personajes_list.append({
            'nombre': nombre,
            'tipo': tipo
        })
        
       # for personajes in personajes_list: 
        data={ 
      #      personajes:personajes
        'personajes': personajes_list
            }
        #    
    for i in data.items():print(i)

    return report(request, 'rep1', data)

def exportReport21(request):
    conexion= connect(host="localhost",database="marveldb",user="postgres",password="12345679")
    cur=conexion.cursor()

    cur.execute("select m.medionombre as nombre, s.serepisodios as episodios "+
                " from infopersonajes.serie s, infopersonajes.medio m "+
                " where (s.medio_id = m.medio_id) "+
                " group by s.medio_id, m.medio_id, s.serepisodios "+ 
                " having s.serepisodios >= (select AVG(s.serepisodios) from infopersonajes.serie s) ; ")

    series_list= []
    #promedio = exportReport20
    #print(promedio)
    for nombre, episodios,  in cur.fetchall():# data={nombre:tipo}promedio
        series_list.append({
            'nombre_medio': nombre,
            'numero_episodios': episodios,
            #'promedio': promedio,
        })
        
       # for personajes in personajes_list: 
    cur.execute("select round(t.promedio,2) "+ " from (select AVG(s.serepisodios) promedio "+" from infopersonajes.serie s) t;")
    promedio = cur.fetchone()[0]
    print(promedio)
    
    data2={ 
      #      personajes:personajes
        'series': series_list,
        'promedio': promedio
            }
        #    
    #for i in data2.items():print(i)

    return  report(request, 'rep2', data2)

def exportReport20():
    conexion= connect(host="localhost",database="marveldb",user="postgres",password="12345679")
    cur=conexion.cursor()

    cur.execute("select AVG(s.serepisodios) promedio "+ " from infopersonajes.serie s ; ")

    #series_list= []
    prom = 0,00
    for promedio in cur.fetchall():# data={nombre:tipo}nombre, episodios,
            prom: promedio
        
    

    return prom

def exportReport3(request):
    conexion= connect(host="localhost",database="marveldb",user="postgres",password="12345679")
    cur=conexion.cursor()

    cur.execute("select t.cmblugar as lugar ,max(contador) "+
                " from (select c.cmblugar, count(c.cmblugar) contador "+
                " from infopersonajes.combate c "+
                " group by c.cmblugar) t "+
                " group by t.cmblugar "+
                " order by max(contador) DESC limit 3;")

    combate_list= []
    for lugar, max in cur.fetchall():# data={nombre:tipo}
        combate_list.append({
            'lugar': lugar,
            'max': max
        })
        
       # for personajes in personajes_list: 
        data1={ 
      #      personajes:personajes
        'combates': combate_list
            }
        #    
    for i in data1.items():print(i)

    return report(request, 'rep3', data1)

def exportReport4(request):
    conexion= connect(host="localhost",database="marveldb",user="postgres",password="12345679")
    cur=conexion.cursor()

    cur.execute("select k.nombre, k.poseedor, k.tipo "+
                    " from(select t.objnombre as nombre,t.nombre_superheroe as poseedor,t.tipo, t.contador "+
                     " from(select o.objnombre, h.nombre_superheroe, p.tipo, count(r.fk_obj_reg_id) contador "+
                         " from infopersonajes.personaje p, infopersonajes.heroe h, infopersonajes.objeto o, infopersonajes.registro_combates r "+
                             " where (p.personaje_id = h.personaje_id) and (p.personaje_id = r.id_pers_reg_id) and (o.obid=r.fk_obj_reg_id) "+
                             " group by h.nombre_superheroe, o.objnombre, p.tipo) t "+
                " UNION all "+
                " select t.objnombre as nombre,t.nombre_supervillano as poseedor ,t.tipo, t.contador "+
                    " from(select o.objnombre, v.nombre_supervillano, p.tipo, count(r.fk_obj_reg_id) contador "+
                        " from infopersonajes.personaje p, infopersonajes.villano v, infopersonajes.objeto o, infopersonajes.registro_combates r "+
                            " where (p.personaje_id = v.personaje_id) and (p.personaje_id = r.id_pers_reg_id) and (o.obid=r.fk_obj_reg_id) "+
                            " group by v.nombre_supervillano, o.objnombre, p.tipo) t) k "+
                 " order by k.contador desc limit 3; ")

    objetos_list= []
    for nombre,poseedor,tipo in cur.fetchall():# data={nombre:tipo}
        objetos_list.append({
            'nombre':nombre,
            'poseedor': poseedor,
            'tipo': tipo
        })
        
       # for personajes in personajes_list: 
        data4={ 
      #      personajes:personajes
            'objetos':objetos_list
            }
        #    
    for i in data4.items():print(i)

    return report(request, 'rep4', data4)

def exportReport6(request):
    conexion= connect(host="localhost",database="marveldb",user="postgres",password="12345679")
    cur=conexion.cursor()

    cur.execute("select m.medionombre as nombre,p.pelduracion as duracion,p.pelcosteprod as coste,p.pelganancias as ganancias, m.medfecestreno as estreno "+
                    " from infopersonajes.pelicula p, infopersonajes.medio m "+
                     " where (p.medio_id = m.medio_id) and (p.pelduracion>150) "+
                         " group by p.medio_id, m.medio_id "+
                             " having p.pelganancias >= (select avg(p2.pelganancias) "+
                             " from infopersonajes.pelicula p2 "+
                " where p2.medtipo ='animada') "+
                " order by p.pelcosteprod desc; ")

    peliculas_list= []
    for nombre, duracion, coste, ganancias, estreno in cur.fetchall():# data={nombre:tipo}
        peliculas_list.append({
            'nombre':nombre,
            'duracion':duracion,
            'coste':coste,
            'ganancias':ganancias,
            'estreno':estreno
        })
        
       # for personajes in personajes_list: 
        data6={ 
      #      personajes:personajes
            'peliculas':peliculas_list
            }
        #    
    for i in data6.items():print(i)

    return report(request, 'rep6', data6)

def exportReport5(request):
    conexion= connect(host="localhost",database="marveldb",user="postgres",password="12345679")
    cur=conexion.cursor()

    cur.execute("select p.ponombre as nombre,p.ponaturaleza as naturaleza,p.podescripcion as descripcion, v.nombre_supervillano as usuario "+
                    " from infopersonajes.villano v, infopersonajes.poder p, infopersonajes.personaje_poder q "+
                     " where (p.podid = q.fk_pod_pers) and (v.personaje_id=q.fk_pers_pod) and (q.hereditario = true) and (p.ponombre like 'Super%'); ")

    poderes_list= []
    for nombre, naturaleza, descripcion, usuario in cur.fetchall():# data={nombre:tipo}
        poderes_list.append({
            'nombre':nombre,
            'naturaleza': naturaleza,
            'descripcion': descripcion,
            'usuario':usuario
        })
        
       # for personajes in personajes_list: 
        data5={ 
      #      personajes:personajes
            'poderes':poderes_list
            }
        #    
    for i in data5.items():print(i)

    return report(request, 'rep5', data5)

def exportReport7(request):
    conexion= connect(host="localhost",database="marveldb",user="postgres",password="12345679")
    cur=conexion.cursor()

    cur.execute("select p.primer_nombre as nombre, p.primer_apellido as apellido, c.creador_nombre as nombrec , c.creador_apellido as apellidoc "+
                    " from(select p.primer_nombre, p.primer_apellido, p.personaje_id "+
                     " from infopersonajes.personaje p "+
                        " where ((p.primer_nombre like 'A%') and (p.primer_apellido like 'A%')) "+
                        " OR ((p.primer_nombre like 'B%') and (p.primer_apellido like 'B%')) "+
                        " OR ((p.primer_nombre like 'C%') and (p.primer_apellido like 'C%')) "+
                        " OR ((p.primer_nombre like 'D%') and (p.primer_apellido like 'D%')) "+
                        " OR ((p.primer_nombre like 'E%') and (p.primer_apellido like 'E%')) "+
                        " OR ((p.primer_nombre like 'F%') and (p.primer_apellido like 'F%')) "+
                        " OR ((p.primer_nombre like 'G%') and (p.primer_apellido like 'G%')) "+
                        " OR ((p.primer_nombre like 'H%') and (p.primer_apellido like 'H%')) "+
                        " OR ((p.primer_nombre like 'I%') and (p.primer_apellido like 'I%')) "+
                        " OR ((p.primer_nombre like 'J%') and (p.primer_apellido like 'J%')) "+
                        " OR ((p.primer_nombre like 'K%') and (p.primer_apellido like 'K%')) "+
                        " OR ((p.primer_nombre like 'L%') and (p.primer_apellido like 'L%')) "+
                        " OR ((p.primer_nombre like 'M%') and (p.primer_apellido like 'M%')) "+
                        " OR ((p.primer_nombre like 'N%') and (p.primer_apellido like 'N%')) "+
                        " OR ((p.primer_nombre like 'O%') and (p.primer_apellido like 'O%')) "+
                        " OR ((p.primer_nombre like 'P%') and (p.primer_apellido like 'P%')) "+
                        " OR ((p.primer_nombre like 'Q%') and (p.primer_apellido like 'Q%')) "+
                        " OR ((p.primer_nombre like 'R%') and (p.primer_apellido like 'R%')) "+
                        " OR ((p.primer_nombre like 'S%') and (p.primer_apellido like 'S%')) "+
                        " OR ((p.primer_nombre like 'T%') and (p.primer_apellido like 'T%')) "+
                        " OR ((p.primer_nombre like 'U%') and (p.primer_apellido like 'U%')) "+
                        " OR ((p.primer_nombre like 'V%') and (p.primer_apellido like 'V%')) "+
                        " OR ((p.primer_nombre like 'W%') and (p.primer_apellido like 'W%')) "+
                        " OR ((p.primer_nombre like 'X%') and (p.primer_apellido like 'X%')) "+
                        " OR ((p.primer_nombre like 'Y%') and (p.primer_apellido like 'Y%')) "+
                        " OR ((p.primer_nombre like 'Z%') and (p.primer_apellido like 'Z%')))p, infopersonajes.creador c "+
                             " where (p.personaje_id = c.id_personaje_cre); ")

    personajes_list= []
    for nombre,apellido, nombrec, apellidoc in cur.fetchall():# data={nombre:tipo}
        personajes_list.append({
            'nombre':nombre,
            'apellido':apellido,
            'nombrec':nombrec,
            'apellidoc':apellidoc
        })
        
       # for personajes in personajes_list: 
        data7={ 
      #      personajes:personajes
            'personajes':personajes_list
            }
        #    
    for i in data7.items():print(i)

    return report(request, 'rep7', data7)

def exportReport8(request):
    conexion= connect(host="localhost",database="marveldb",user="postgres",password="12345679")
    cur=conexion.cursor()

    cur.execute("select o.org_nombre as org, p.primer_nombre as nombrelider, p.primer_apellido as apellidolider, org.contador1 as sedes, pers.contador2 as orgs "+
                    " from (select o.id_organizacion, count(s.org_id) contador1 "+
                     " from infopersonajes.organizacion o, infopersonajes.sede s "+
                         " where (o.id_organizacion=s.org_id) "+
                             " group by s.org_id, o.id_organizacion "+
                             "  order by contador1 desc) org, (select p.personaje_id, count(h.fk_pers_org) contador2 "+
                " from infopersonajes.personaje p, infopersonajes.historico_personaje h "+
                " where (p.personaje_id=h.fk_pers_org) "+
                " group by h.fk_pers_org, p.personaje_id "+
                " order by contador2 desc) pers, infopersonajes.personaje p, infopersonajes.organizacion o, infopersonajes.historico_personaje h "+
                " where (p.personaje_id=pers.personaje_id) and (org.id_organizacion=o.id_organizacion) and (h.fk_org_pers=org.id_organizacion) and (h.fk_pers_org=pers.personaje_id) and (h.lider=true) and (pers.contador2>=2) and (org.contador1>2); ")

    organizaciones_list= []
    for org, nombrelider, apellidolider, sedes, orgs in cur.fetchall():# data={nombre:tipo}
        organizaciones_list.append({
            'org': org,
            'nombrelider': nombrelider,
            'apellidolider': apellidolider,
            'sedes': sedes,
            'orgs': orgs
        })
        
       # for personajes in personajes_list: 
        data8={ 
      #      personajes:personajes
            'organizaciones': organizaciones_list
            }
        #    
    for i in data8.items():print(i)

    return report(request, 'rep8', data8)

def Home(request):
    return render(request, 'home.html')


def Singup(request):
    if request.method == 'GET':
        return render(request, 'singup.html', {
            'form': UsuarioForm
        })
    else:
        if request.POST['password'] == request.POST['password2']:
            try:
                user = Usuario.objects.create_user(
                    username=request.POST['username'], password=request.POST['password'],
                    nombreu=request.POST['nombreu'], apellidou=request.POST['apellidou'],
                    correou=request.POST['correou'],fechanacu=request.POST['fechanacu'],
                    ciudadu=request.POST['ciudadu'],sexou=request.POST['sexou'],paisu=request.POST['paisu'])
                user.save()
                login(request,user)
                for i in range(1,6):
                    Perfil.objects.create(idioma='Español',percorreo=user.correou,fk_usuario=user)
                messages.success(request,"usuario creado con exito")
                return redirect('sub')
            except IntegrityError:
                return render(request, 'singup.html', {
                    'form': UsuarioForm,
                    'error':'ERROR: Dato invalido revise los datos ingresados'
                })
        else:
            return render(request, 'singup.html', {
                    'form': UsuarioForm,
                    'error':'Las contraseñas no coinciden'
            })
        
def singin(request):
    if request.method == 'GET':
        return render(request,'singin.html',{
            'form':LoginForm
        })    
    else:
        user = authenticate(request,username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request,'singin.html',{
                'form':LoginForm,
                'error':'Usuario o contraseña es incorrecto'
            }) 
        else:
            login(request,user)
            p = Perfil.objects.filter(fk_usuario=user).count()
            if p != 5:
                for i in range(1,6-p):
                    Perfil.objects.create(idioma='Español',percorreo=user.correou,fk_usuario=user)
            messages.success(request,"Inició sesión con exito")
            if user.sub_fk:
                return redirect('escoger_perfil')
            else:
                return redirect('sub')

@login_required
def singout(request):
    user = request.user
    desper = get_object_or_404(Perfil,fk_usuario=user,esta_activo=True)
    act = Actividad.objects.filter(fk_perfil=desper).order_by('-act_ingreso').first()
    act.act_fin = timezone.now()
    act.save()
    desper.esta_activo = False
    desper.save()
    logout(request)
    messages.success(request,"Cerró sesión con exito")
    return redirect('home')

@login_required
def seleccionar_subscripcion(request):
    if request.method == 'GET':
        gold = Suscripcion.objects.filter(sustipo='Gold')
        prem = Suscripcion.objects.filter(sustipo='Premium')
        vip = Suscripcion.objects.filter(sustipo='VIP')
        bengold = Beneficio.objects.raw(
            "select b.benid, bendescripcion from infousuarios.beneficio b inner join infousuarios.suscripcion_beneficio sb on b.benid = sb.fk_ben_sus inner join infousuarios.suscripcion s on  s.susid = sb.fk_sus_ben where sustipo like 'Gold'")
        benprem = Beneficio.objects.raw(
            "select b.benid, bendescripcion from infousuarios.beneficio b inner join infousuarios.suscripcion_beneficio sb on b.benid = sb.fk_ben_sus inner join infousuarios.suscripcion s on s.susid = sb.fk_sus_ben where sustipo like 'Premium'")
        benvip = Beneficio.objects.raw(
            "select b.benid, bendescripcion from infousuarios.beneficio b inner join infousuarios.suscripcion_beneficio sb on b.benid = sb.fk_ben_sus inner join infousuarios.suscripcion s on  s.susid = sb.fk_sus_ben where sustipo like 'VIP'")
        return render(request,'select_sub.html',{
            'gold':gold,
            'prem':prem,
            'vip':vip,
            'bengold':bengold,
            'benprem':benprem,
            'benvip':benvip,
        })

@login_required
def registrar_subscripcion(request,susid):
    sub = get_object_or_404(Suscripcion,pk=susid)
    if request.method == 'POST':
        user = request.user
        user.sub_fk = sub
        user.save()
        comtdc = Tarjetacredito.objects.filter(fk_usuario=user)
        messages.success(request,"Subscripcion registrada con exito")
        if comtdc:
            return redirect('escoger_perfil')
        else:
            return redirect('newtdc')

@login_required
def registro_tdc(request):
    if request.method == 'GET':
        return render(request,'registrar_tarjeta.html', {
            'form': TDCForm,           
        })
    else:
        try:
            form = TDCForm(request.POST)
            NewTdc = form.save(commit=False)
            NewTdc.fk_usuario = request.user
            NewTdc.save()
            messages.success(request,"Tarjeta registrada con exito")
            return redirect('escoger_perfil')
        except ValueError:
            return render(request,'registrar_tarjeta.html', {
                'form': TDCForm,
                'error':'Por favor ingrese datos validos'           
            })
        
@login_required
def escoger_perfl(request):
    user = request.user
    perf = Perfil.objects.filter(fk_usuario=user)
    return render(request,'esc_perfil.html', {'Perfiles': perf})

def activo_perfil(request,pf_id):
    perf = get_object_or_404(Perfil, pk=pf_id)
    perf.esta_activo = True
    perf.save()
    if request.user_agent.is_mobile:
        dis=request.user_agent.device.family
    elif request.user_agent.is_tablet:
        dis=request.user_agent.device.family
    elif request.user_agent.is_pc:
        dis='PC'
    act = Actividad.objects.create(act_ingreso=timezone.now(),fk_perfil=perf,act_dispositivo=dis)
    act.save()
    messages.success(request,"Escogió el perfil con exito")
    return redirect('home')

@login_required
def Civiles(request):
    civiles = Personaje.objects.raw(
        "select p.personaje_id, genc, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, color_pelo,color_ojos, frase_celebre, comic_primer_vez, estadomarital from infopersonajes.personaje p inner join infopersonajes.civil c on p.personaje_id = c.personaje_id")
    return render(request,'civiles.html',{
        'civiles':civiles,
    })

@login_required
def new_civil(request):
    if request.method == 'GET':
        return render(request,'new_civil.html', {
            'form': PersonajeForm,           
        })
    else:
        try:
            form = PersonajeForm(request.POST)
            NewCiv = form.save(commit=False)
            NewCiv.save()
            civil = Civil.objects.create(personaje=NewCiv)
            civil.save()
            messages.success(request,"Civil creado con exito")
            return redirect('civiles')
        except ValueError:
            return render(request,'new_civil.html', {
                'form': PersonajeForm,
                'error':'Por favor ingrese datos validos'           
            })
        

@login_required
def elimina_civil(request,civil_id):
    try:
        civ = Civil.objects.filter(personaje=civil_id)
        pers = Personaje.objects.filter(personaje_id=civil_id)
        civ.delete()
        pers.delete()
        messages.success(request,"Civil borrado con exito")
        return redirect('civiles')  
    except :
        messages.error(request,"Civil no se puede borrar, es referenciado en otras tablas")
        return redirect('civiles') 

@login_required
def actualiza_civil(request,civil_id):
    civil = get_object_or_404(Personaje,pk=civil_id)
    if request.method == 'GET':
        form = PersonajeForm(instance=civil)
        return render(request,'act_civil.html', {'civil': civil,'form': form })
    else:
        try:
            form = PersonajeForm(request.POST,instance=civil)
            form.save()
            messages.success(request,"Civil actualizado con exito")
            return redirect('civiles')
        except ValueError:
            return render(request,'act_civil.html', {'civil': civil,'form': form,
                'error':"ERROR. No se ha podido actualizar"
            }) 

@login_required
def Heroes(request):
    heroes = Personaje.objects.raw(
        "select p.personaje_id, genc, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, color_pelo,color_ojos, frase_celebre, comic_primer_vez, estadomarital from infopersonajes.personaje p inner join infopersonajes.heroe h on p.personaje_id = h.personaje_id")
    hinfo = Heroe.objects.all()
    return render(request,'heroes.html',{
        'heroes':heroes,
        'hinfo':hinfo
    })

@login_required
def elimina_heroe(request,heroe_id):
    try:
        hero = get_object_or_404(Heroe,pk=heroe_id)
        pers = get_object_or_404(Personaje,pk=heroe_id)
        hero.delete()
        pers.delete()
        messages.success(request,"Heroe eliminado con exito")
        return redirect('heroes')
    except:
        messages.error(request,"Heroe no se puede borrar, es referenciado en otras tablas")
        return redirect('heroes')

@login_required
def new_heroe(request):
    if request.method == 'GET':
        return render(request,'new_heroe.html', {
            'form': PersonajeForm,
            'form2': HeroeForm,           
        })
    else:
        try:
            form = PersonajeForm(request.POST)
            form2 = HeroeForm(request.POST)
            NewHer = form.save(commit=False)
            hero = form2.save(commit=False)
            NewHer.save()
            hero.personaje = NewHer
            hero.save()
            messages.success(request,"Heroe creado con exito")
            return redirect('heroes')
        except ValueError:
            return render(request,'new_heroe.html', {
                'form': PersonajeForm,
                'form2': HeroeForm,
                'error':'Por favor ingrese datos validos'           
            })
        

@login_required
def actualiza_heroe(request,heroe_id):
    pers = get_object_or_404(Personaje,pk=heroe_id)
    hero = get_object_or_404(Heroe,pk=heroe_id)
    if request.method == 'GET':
        form = PersonajeForm(instance=pers)
        form2 = HeroeForm(instance=hero)
        return render(request,'act_heroe.html', {'heroe': pers,'adinfo':hero,'form': form,'form2': form2 })
    else:
        try:
            form = PersonajeForm(request.POST,instance=pers)
            form2 = HeroeForm(request.POST,instance=hero)
            form.save()
            form2.save()
            messages.success(request,"Heroe actualizado con exito")
            return redirect('heroes')
        except ValueError:
            return render(request,'act_heroe.html', {'heroe': pers,'adinfo':hero,'form': form,'form2': form2,'error':"ERROR. No se ha podido actualizar"}) 
        
@login_required
def villanos(request):
    vil = Personaje.objects.raw(
        "select p.personaje_id, genc, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, color_pelo,color_ojos, frase_celebre, comic_primer_vez, estadomarital from infopersonajes.personaje p inner join infopersonajes.villano v on p.personaje_id = v.personaje_id")
    vinfo = Villano.objects.all()
    return render(request,'villanos.html',{
        'villanos':vil,
        'vinfo':vinfo
    })

@login_required
def elimina_villano(request,vil_id):
    vil = get_object_or_404(Villano,pk=vil_id)
    pers = get_object_or_404(Personaje,pk=vil_id)
    try:
        vil.delete()
        pers.delete()
        messages.success(request,"Villano eliminado con exito")
        return redirect('villanos')  
    except:
        vil.personaje = pers
        vil.save()
        messages.error(request,"Villano no se puede borrar, es referenciado en otras tablas")
        return redirect('villanos')  

@login_required
def new_villano(request):
    if request.method == 'GET':
        return render(request,'new_villano.html', {
            'form': PersonajeForm,
            'form2': VilanoForm,           
        })
    else:
        try:
            form = PersonajeForm(request.POST)
            form2 = VilanoForm(request.POST)
            NewVil = form.save(commit=False)
            vil = form2.save(commit=False)
            NewVil.save()
            vil.personaje = NewVil
            vil.save()
            messages.success(request,"Villano creado con exito")
            return redirect('villanos')
        except ValueError:
            return render(request,'new_villano.html', {
                'form': PersonajeForm,
                'form2': VilanoForm,
                'error':'Por favor ingrese datos validos'           
            })
        
@login_required
def actualiza_vilano(request,vil_id):
    pers = get_object_or_404(Personaje,pk=vil_id)
    vil = get_object_or_404(Villano,pk=vil_id)
    if request.method == 'GET':
        form = PersonajeForm(instance=pers)
        form2 = VilanoForm(instance=vil)
        return render(request,'act_villano.html', {'villano': pers,'adinfo':vil,'form': form,'form2': form2 })
    else:
        try:
            form = PersonajeForm(request.POST,instance=pers)
            form2 = VilanoForm(request.POST,instance=vil)
            form.save()
            form2.save()
            messages.success(request,"Villano actualizado con exito")
            return redirect('villanos')
        except ValueError:
            return render(request,'act_villano.html', {'villano': pers,'adinfo':vil,'form': form,'form2': form2,'error':"ERROR. No se ha podido actualizar"}) 
        

@login_required
def peliculas(request):
    pel = Medio.objects.raw("select m.medio_id, medfecestreno, medcomcreacion, medcomproduc, medrating, medsinopsis, medionombre from infopersonajes.medio m inner join infopersonajes.pelicula p on m.medio_id = p.medio_id")
    pinfo = Pelicula.objects.all()
    return render(request,'peliculas.html',{
        'peliculas':pel,
        'pinfo':pinfo
    })

@login_required
def elimina_pelicula(request,pel_id):
    pel = get_object_or_404(Pelicula,pk=pel_id)
    med = get_object_or_404(Medio,pk=pel_id)
    try:
        pel.delete()
        med.delete()
        messages.success(request,"Pelicula eliminada con exito")
        return redirect('peliculas')
    except:
        pel.medio = med
        pel.save()
        messages.error(request,"Pelicula no se puede borrar, es referenciada en otras tablas")
        return redirect('peliculas') 


@login_required
def new_pelicula(request):
    if request.method == 'GET':
        return render(request,'new_pelicula.html', {
            'form': MedioForm,
            'form2': PeliForm,           
        })
    else:
        try:
            form = MedioForm(request.POST)
            form2 = PeliForm(request.POST)
            NewPel = form.save(commit=False)
            peli = form2.save(commit=False)
            NewPel.tipomed = 'Pelicula'
            NewPel.save()
            peli.medio = NewPel
            peli.save()
            messages.success(request,"Pelicula creada con exito")
            return redirect('peliculas')
        except ValueError:
            return render(request,'new_pelicula.html', {
                'form': MedioForm,
                'form2': PeliForm,
                'error':'Por favor ingrese datos validos'           
            })
        
@login_required
def actualiza_pelicula(request,pel_id):
    pel = get_object_or_404(Pelicula,pk=pel_id)
    med = get_object_or_404(Medio,pk=pel_id)
    if request.method == 'GET':
        form = MedioForm(instance=med)
        form2 = PeliForm(instance=pel)
        return render(request,'act_pelicula.html', {'pelicula': med,'adinfo':pel,'form': form,'form2': form2 })
    else:
        try:
            form = MedioForm(request.POST,instance=med)
            form2 = PeliForm(request.POST,instance=pel)
            form.save()
            form2.save()
            messages.success(request,"Pelicula actualizada con exito")
            return redirect('peliculas')
        except ValueError:
            return render(request,'act_pelicula.html', {'pelicula': med,'adinfo':pel,'form': form,'form2': form2, 'error':"ERROR. No se ha podido actualizar"}) 

@login_required
def series(request):
    ser = Medio.objects.raw("select m.medio_id, medfecestreno, medcomcreacion, medcomproduc, medrating, medsinopsis, medionombre from infopersonajes.medio m inner join infopersonajes.serie s on m.medio_id = s.medio_id")
    seinfo = Serie.objects.all()
    return render(request,'series.html',{
        'series':ser,
        'sinfo':seinfo
    })

@login_required
def elimina_serie(request,se_id):
    ser = get_object_or_404(Serie,pk=se_id)
    med = get_object_or_404(Medio,pk=se_id)
    try:
        ser.delete()
        med.delete()
        messages.success(request,"Serie eliminada con exito")
        return redirect('series')
    except:
        ser.medio = med
        ser.save()
        messages.error(request,"Serie no se puede borrar, es referenciada en otras tablas")
        return redirect('series')   


@login_required
def new_serie(request):
    if request.method == 'GET':
        return render(request,'new_serie.html', {
            'form': MedioForm,
            'form2': SerieForm,           
        })
    else:
        try:
            form = MedioForm(request.POST)
            form2 = SerieForm(request.POST)
            NewSer = form.save(commit=False)
            ser = form2.save(commit=False)
            NewSer.tipomed = 'Serie'
            NewSer.save()
            ser.medio = NewSer
            ser.save()
            messages.success(request,"Serie Creada con exito")
            return redirect('series')
        except ValueError:
            return render(request,'new_serie.html', {
                'form': MedioForm,
                'form2': SerieForm,
                'error':'Por favor ingrese datos validos'           
            })
        
@login_required
def actualiza_serie(request,se_id):
    ser = get_object_or_404(Serie,pk=se_id)
    med = get_object_or_404(Medio,pk=se_id)
    if request.method == 'GET':
        form = MedioForm(instance=med)
        form2 = SerieForm(instance=ser)
        return render(request,'act_serie.html', {'serie': med,'adinfo':ser,'form': form,'form2': form2 })
    else:
        try:
            form = MedioForm(request.POST,instance=med)
            form2 = SerieForm(request.POST,instance=ser)
            form.save()
            form2.save()
            messages.success(request,"Serie actualizada con exito")
            return redirect('series')
        except ValueError:
            return render(request,'act_pelicula.html', {'serie': med,'adinfo':ser,'form': form,'form2': form2, 'error':"ERROR. No se ha podido actualizar"}) 
        
@login_required
def juegos(request):
    juego = Medio.objects.raw("select m.medio_id, medfecestreno, medcomcreacion, medcomproduc, medrating, medsinopsis, medionombre from infopersonajes.medio m inner join infopersonajes.juego j on m.medio_id = j.medio_id")
    vdinfo = Juego.objects.all()
    return render(request,'juegos.html',{
        'juegos':juego,
        'vdinfo':vdinfo
    })

@login_required
def elimina_juego(request,jue_id):
    jue = get_object_or_404(Juego,pk=jue_id)
    med = get_object_or_404(Medio,pk=jue_id)
    try:
        jue.delete()
        med.delete()
        messages.success(request,"Juego eliminado con exito")
        return redirect('juegos') 
    except:
        jue.medio = med
        jue.save()
        messages.error(request,"Juego no se puede borrar, es referenciado en otras tablas")
        return redirect('juegos')  


@login_required
def new_juego(request):
    if request.method == 'GET':
        return render(request,'new_juego.html', {
            'form': MedioForm,
            'form2': JuegoForm,           
        })
    else:
        try:
            form = MedioForm(request.POST)
            form2 = JuegoForm(request.POST)
            NewJue = form.save(commit=False)
            jue = form2.save(commit=False)
            NewJue.tipomed = 'Juego'
            NewJue.save()
            jue.medio = NewJue
            jue.save()
            messages.success(request,"Juego creado con exito")
            return redirect('juegos')
        except ValueError:
            return render(request,'new_juego.html', {
                'form': MedioForm,
                'form2': JuegoForm,
                'error':'Por favor ingrese datos validos'           
            })
        
@login_required
def actualiza_juego(request,jue_id):
    jue = get_object_or_404(Juego,pk=jue_id)
    med = get_object_or_404(Medio,pk=jue_id)
    if request.method == 'GET':
        form = MedioForm(instance=med)
        form2 = JuegoForm(instance=jue)
        return render(request,'act_juego.html', {'juego': med,'adinfo':jue,'form': form,'form2': form2 })
    else:
        try:
            form = MedioForm(request.POST,instance=med)
            form2 = JuegoForm(request.POST,instance=jue)
            form.save()
            form2.save()
            messages.success(request,"Juego actualizado con exito")
            return redirect('juegos')
        except ValueError:
            return render(request,'act_pelicula.html', {'juego': med,'adinfo':jue,'form': form,'form2': form2, 'error':"ERROR. No se ha podido actualizar"}) 

@login_required
def organizaciones(request):
    org = Organizacion.objects.all()
    return render(request,'organizaciones.html',{
        'orgs':org,
    })

@login_required
def elimina_organizacion(request,org_id):
    try:
        org = get_object_or_404(Organizacion,pk=org_id)
        org.delete()
        messages.success(request,"Organización eliminada con exito")
        return redirect('organizaciones')
    except:
        messages.error(request,"Organización no se puede borrar, es referenciada en otras tablas")
        return redirect('organizaciones')    

@login_required
def new_organizacion(request):
    if request.method == 'GET':
        return render(request,'new_organizacion.html', {
            'form': OrganizacionForm,          
        })
    else:
        try:
            form = OrganizacionForm(request.POST)
            NewOrg = form.save(commit=False)
            NewOrg.save()
            messages.success(request,"Organización creada con exito")
            return redirect('organizaciones')
        except ValueError:
            return render(request,'new_organizacion.html', {
                'form': OrganizacionForm, 
                'error':'Por favor ingrese datos validos'           
            })
        
@login_required
def actualiza_organizacion(request,org_id):
    Org = get_object_or_404(Organizacion,pk=org_id)
    if request.method == 'GET':
        form = OrganizacionForm(instance=Org)
        return render(request,'act_organizacion.html', {'organizacion': Org,'form': form})
    else:
        try:
            form = OrganizacionForm(request.POST,instance=Org)
            form.save()
            messages.success(request,"Organización actualizada con exito")
            return redirect('organizaciones')
        except ValueError:
            return render(request,'act_organizacion.html', {'organizacion': Org,'form': form, 'error':"ERROR. No se ha podido actualizar"}) 
        
@login_required
def sedes(request):
    sed = Sede.objects.all()
    return render(request,'sedes.html',{
        'sedes':sed,
    })

@login_required
def elimina_sede(request,sed_id):
    try:
        sed = get_object_or_404(Sede,pk=sed_id)
        sed.delete()
        messages.success(request,"Sede eliminada con exito")
        return redirect('sedes')
    except:
        messages.error(request,"Sede no se puede borrar, es referenciada en otras tablas")
        return redirect('sedes') 

@login_required
def new_sede(request):
    if request.method == 'GET':
        return render(request,'new_sede.html', {
            'form': SedeForm,          
        })
    else:
        try:
            form = SedeForm(request.POST)
            NewSed = form.save(commit=False)
            NewSed.save()
            messages.success(request,"Sede creada con exito")
            return redirect('sedes')
        except ValueError:
            return render(request,'new_sede.html', {
                'form': SedeForm, 
                'error':'Por favor ingrese datos validos'           
            })
        
@login_required
def actualiza_sede(request,sed_id):
    sed = get_object_or_404(Sede,pk=sed_id)
    if request.method == 'GET':
        form = SedeForm(instance=sed)
        return render(request,'act_sede.html', {'sede': sed,'form': form})
    else:
        try:
            form = SedeForm(request.POST,instance=sed)
            form.save()
            messages.success(request,"Sede actualizada con exito")
            return redirect('sedes')
        except ValueError:
            return render(request,'act_sede.html', {'sede': sed,'form': form, 'error':"ERROR. No se ha podido actualizar"}) 
        
@login_required
def poderes(request):
    pod = Poder.objects.all()
    return render(request,'poderes.html',{
        'poderes':pod,
    })

@login_required
def elimina_poder(request,pod_id):
    try:
        pod = get_object_or_404(Poder,pk=pod_id)
        pod.delete()
        messages.success(request,"Poder eliminado con exito")
        return redirect('poderes')  
    except:
        messages.error(request,"Poder no se puede borrar, es referenciado en otras tablas")
        return redirect('poderes') 

@login_required
def new_poder(request):
    if request.method == 'GET':
        return render(request,'new_poder.html', {
            'form': PoderForm,          
        })
    else:
        try:
            form = PoderForm(request.POST)
            NewPod = form.save(commit=False)
            NewPod.save()
            messages.success(request,"Poder creado con exito")
            return redirect('poderes')
        except ValueError:
            return render(request,'new_poder.html', {
                'form': PoderForm, 
                'error':'Por favor ingrese datos validos'           
            })
        
@login_required
def actualiza_poder(request,pod_id):
    pod = get_object_or_404(Poder,pk=pod_id)
    if request.method == 'GET':
        form = PoderForm(instance=pod)
        return render(request,'act_poder.html', {'poder': pod,'form': form})
    else:
        try:
            form = PoderForm(request.POST,instance=pod)
            form.save()
            messages.success(request,"Poder actualizado con exito")
            return redirect('poderes')
        except ValueError:
            return render(request,'act_poder.html', {'poder': pod,'form': form, 'error':"ERROR. No se ha podido actualizar"}) 
        
@login_required
def objetos(request):
    obj = Objeto.objects.all()
    return render(request,'objetos.html',{
        'objetos':obj,
    })

@login_required
def elimina_objeto(request,obj_id):
    try:
        obj = get_object_or_404(Objeto,pk=obj_id)
        obj.delete()
        messages.success(request,"Objeto eliminado con exito")
        return redirect('objetos')
    except:
        messages.error(request,"Objeto no se puede borrar, es referenciado en otras tablas")
        return redirect('objetos') 

@login_required
def new_objeto(request):
    if request.method == 'GET':
        return render(request,'new_objeto.html', {
            'form': ObjetoForm,          
        })
    else:
        try:
            form = ObjetoForm(request.POST)
            NewObj = form.save(commit=False)
            NewObj.save()
            messages.success(request,"Objeto creado con exito")
            return redirect('objetos')
        except ValueError:
            return render(request,'new_objeto.html', {
                'form': ObjetoForm, 
                'error':'Por favor ingrese datos validos'           
            })
        
@login_required
def actualiza_objeto(request,obj_id):
    obj = get_object_or_404(Objeto,pk=obj_id)
    if request.method == 'GET':
        form = ObjetoForm(instance=obj)
        return render(request,'act_objeto.html', {'objeto': obj,'form': form})
    else:
        try:
            form = ObjetoForm(request.POST,instance=obj)
            form.save()
            messages.success(request,"Objeto actualizado con exito")
            return redirect('objetos')
        except ValueError:
            return render(request,'act_objeto.html', {'objeto': obj,'form': form, 'error':"ERROR. No se ha podido actualizar"}) 

@login_required
def Lista_guardados(request):
    per = get_object_or_404(Perfil,fk_usuario=request.user,esta_activo=True)
    med = PerfilMedio.objects.filter(fk_perf_med=per)
    return render(request,'listguar.html',{
        'medios':med,
    })

@login_required
def lg_eliminar(request,med_id):
    Permed = get_object_or_404(PerfilMedio,pk=med_id)
    Permed.delete()
    messages.success(request,"Quitado de la lista con exito")
    return redirect('listguardados')

@login_required
def lg_guardar(request,med_id):
    per = get_object_or_404(Perfil,fk_usuario=request.user,esta_activo=True)
    med = get_object_or_404(Medio,pk=med_id)
    Permed = PerfilMedio.objects.create(fk_perf_med=per,fk_med_perf=med,fecha_vista=timezone.now())
    Permed.save()
    messages.success(request,"Agregado a la lista con exito")
    return redirect('lg_calificar',Permed.id)

@login_required
def lg_calificar(request,med_id):
    Permed = get_object_or_404(PerfilMedio,pk=med_id)
    if request.method == 'GET':
        form = CalMedioForm(instance=Permed)
        return render(request,'cal_medio.html', {'medio': Permed,'form': form})
    else:
        try:
            form = CalMedioForm(request.POST,instance=Permed)
            form.save()
            messages.success(request,"Calificado con exito")
            return redirect('listguardados')
        except ValueError:
            return render(request,'cal_medio.html', {'medio': Permed,'form': form, 'error':"ERROR. No se ha podido actualizar"}) 

@login_required
def combates(request):
    comb = Combate.objects.all()
    cmbinfo = RegistroCombates.objects.all()
    return render(request,'combates.html',{
        'combates':comb,
        'cmbinfo':cmbinfo
    })

@login_required
def cmb_elimina(request,cmb_id):
    cmb = get_object_or_404(Combate,pk=cmb_id)
    Regcmb = RegistroCombates.objects.filter(fk_cmb_reg=cmb_id)
    cmb.delete()
    Regcmb.delete()
    messages.success(request,"Combate eliminado con exito")
    return redirect('combates')

@login_required
def new_combate(request):
    if request.method == 'GET':
        return render(request,'new_combate.html', {
            'form': CombateForm,
            'form2': CmbRegForm,
            'form3': CmbRegForm,           
        })
    else:
        try:
            form = CombateForm(request.POST)
            form2 = CmbRegForm(request.POST)
            form3 = CmbRegForm(request.POST)
            NewCmb = form.save(commit=False)
            com1 = form2.save(commit=False)
            com2 = form3.save(commit=False)
            NewCmb.save()
            com1.fk_cmb_reg = NewCmb
            com2.fk_cmb_reg = NewCmb
            com1.save()
            com2.save()
            messages.success(request,"Combate creado con exito")
            return redirect('combates')
        except ValueError:
            return render(request,'new_combate.html', {
                'form': CombateForm,
                'form2': CmbRegForm,
                'form3': CmbRegForm,
                'error':'Por favor ingrese datos validos'           
            })

@login_required
def actualiza_combate(request,cmb_id):
    cmb = get_object_or_404(Juego,pk=cmb_id)
    cmbone = RegistroCombates.objects.filter(fk_cmb_reg=cmb_id).first()
    cmbtwo = RegistroCombates.objects.filter(fk_cmb_reg=cmb_id).last()
    if request.method == 'GET':
        form = CombateForm(instance=cmb)
        form2 = CmbRegForm(instance=cmbone)
        form3 = CmbRegForm(instance=cmbtwo)
        return render(request,'act_combate.html', {'combate': cmb,'cmb1':cmbone,'cmb2':cmbtwo,'form': form,'form2': form2,'form3': form3 })
    else:
        try:
            form = CombateForm(instance=cmb)
            form2 = CmbRegForm(instance=cmbone)
            form3 = CmbRegForm(instance=cmbtwo)
            form.save()
            form2.save()
            form3.save()
            messages.success(request,"Combate actualizado con exito")
            return redirect('combates')
        except ValueError:
            return render(request,'act_combate.html', {'combate': cmb,'cmb1':cmbone,'cmb2':cmbtwo,'form': form,'form2': form2,'form3': form3, 'error':"ERROR. No se ha podido actualizar"}) 

@login_required
def recom_menu(request):
    return render(request,'recomenu.html')

@login_required
def actividad_admin(request):
    act = Actividad.objects.all()
    return render(request,'actividad.html',{
        'actividad':act,
    })

@login_required
def recom_mejores(request):
    per = get_object_or_404(Perfil,fk_usuario=request.user,esta_activo=True)
    med = Medio.objects.raw("select m.medio_id, medfecestreno, medcomcreacion, medcomproduc, medrating, medsinopsis, medionombre, tipomed from infopersonajes.medio m where medrating between 4 and 5 and medio_id not in (select fk_med_perf_id from infousuarios.perfil_medio where fk_perf_med_id ="+str(per.per_id)+");")

    return render(request,'mejores.html',{
        'medios':med,
    })

@login_required
def recom_nuevas(request):
    per = get_object_or_404(Perfil,fk_usuario=request.user,esta_activo=True)
    med = Medio.objects.raw("SELECT m.medio_id, medfecestreno, medcomcreacion, medcomproduc, medrating, medsinopsis, medionombre, tipomed FROM infopersonajes.medio m WHERE medfecestreno >= (now() - interval '3 months') and medio_id not in (select fk_med_perf_id from infousuarios.perfil_medio where fk_perf_med_id ="+str(per.per_id)+");")
    return render(request,'nuevas.html',{
        'medios':med,
    })


@login_required
def amistades(request):
    ami = Amistad.objects.all()
    return render(request,'amistades.html',{
        'amistades':ami,
    })

@login_required
def elimina_amistad(request,ami_id):
    ami = get_object_or_404(Amistad,pk=ami_id)
    ami.delete()
    messages.success(request,"Amistad eliminada con exito")
    return redirect('amistades')  

@login_required
def new_amistad(request):
    if request.method == 'GET':
        return render(request,'new_amistad.html', {
            'form': AmistadForm,          
        })
    else:
        try:
            form = AmistadForm(request.POST)
            NewAmi = form.save(commit=False)
            NewAmi.save()
            messages.success(request,"Amistad creada con exito")
            return redirect('amistades')
        except ValueError:
            return render(request,'new_amistad.html', {
                'form': AmistadForm, 
                'error':'Por favor ingrese datos validos'           
            })

@login_required
def matrimonios(request):
    mat = HistoricoMatrimonio.objects.all()
    return render(request,'matrimonios.html',{
        'matrimonios':mat,
    })

@login_required
def elimina_matrimonio(request,mat_id):
    mat = get_object_or_404(HistoricoMatrimonio,pk=mat_id)
    mat.delete()
    messages.success(request,"Matrimonio eliminado con exito")
    return redirect('matrimonios')  

@login_required
def new_matrimonio(request):
    if request.method == 'GET':
        return render(request,'new_matrimonio.html', {
            'form': MatrimonioForm,          
        })
    else:
        try:
            form = MatrimonioForm(request.POST)
            NewMat = form.save(commit=False)
            NewMat.save()
            messages.success(request,"Matrimonio creado con exito")
            return redirect('matrimonios')
        except ValueError:
            return render(request,'new_matrimonio.html', {
                'form': MatrimonioForm, 
                'error':'Por favor ingrese datos validos'           
            })
        
@login_required
def actualiza_matrimonio(request,mat_id):
    mat = get_object_or_404(HistoricoMatrimonio,pk=mat_id)
    if request.method == 'GET':
        form = MatrimonioForm(instance=mat)
        return render(request,'act_matrimonio.html', {'matrimonio': mat,'form': form})
    else:
        try:
            form = MatrimonioForm(request.POST,instance=mat)
            form.save()
            messages.success(request,"Matrimonio actualizado con exito")
            return redirect('matrimonios')
        except ValueError:
            return render(request,'act_matrimonio.html', {'matrimonio': mat,'form': form, 'error':"ERROR. No se ha podido actualizar"}) 

@login_required
def Histpersonajes(request):
    hit = HistoricoPersonaje.objects.all()
    return render(request,'Histpersonajes.html',{
        'historico':hit,
    })

@login_required
def elimina_histpersonaje(request,hit_id):
    hit = get_object_or_404(HistoricoPersonaje,pk=hit_id)
    hit.delete()
    messages.success(request,"Historico del personaje eliminado con exito")
    return redirect('histpersonajes')

@login_required
def new_histpersonaje(request):
    if request.method == 'GET':
        return render(request,'new_histpersonaje.html', {
            'form': HistPersonajeForm,          
        })
    else:
        try:
            form = HistPersonajeForm(request.POST)
            NewHit = form.save(commit=False)
            NewHit.save()
            messages.success(request,"Historico del personaje creado con exito")
            return redirect('histpersonajes')
        except ValueError:
            return render(request,'new_histpersonaje.html', {
                'form': HistPersonajeForm, 
                'error':'Por favor ingrese datos validos'           
            })
        
@login_required
def actualiza_histpersonaje(request,hit_id):
    hit = get_object_or_404(HistoricoPersonaje,pk=hit_id)
    if request.method == 'GET':
        form = HistPersonajeForm(instance=hit)
        return render(request,'act_histpersonaje.html', {'historico': hit,'form': form})
    else:
        try:
            form = HistPersonajeForm(request.POST,instance=hit)
            form.save()
            messages.success(request,"Historico del personaje actualizado con exito")
            return redirect('histpersonajes')
        except ValueError:
            return render(request,'act_histpersonaje.html', {'historico': hit,'form': form, 'error':"ERROR. No se ha podido actualizar"}) 


@login_required
def Perpoderes(request):
    pp = PersonajePoder.objects.all()
    return render(request,'perpoderes.html',{
        'perspod':pp,
    })

@login_required
def elimina_perpoder(request,pp_id):
    pp = get_object_or_404(PersonajePoder,pk=pp_id)
    pp.delete()
    messages.success(request,"Registro de poder del personaje eliminado con exito")
    return redirect('perpoderes')

@login_required
def new_perpoder(request):
    if request.method == 'GET':
        return render(request,'new_perpoder.html', {
            'form': PerPodForm,          
        })
    else:
        try:
            form = PerPodForm(request.POST)
            Newpp = form.save(commit=False)
            Newpp.save()
            messages.success(request,"Registro de poder del personaje creado con exito")
            return redirect('perpoderes')
        except ValueError:
            return render(request,'new_perpoder.html', {
                'form': PerPodForm, 
                'error':'Por favor ingrese datos validos'           
            })
        
@login_required
def actualiza_perpoder(request,pp_id):
    pp = get_object_or_404(PersonajePoder,pk=pp_id)
    if request.method == 'GET':
        form = PerPodForm(instance=pp)
        return render(request,'act_perpoder.html', {'perpod': pp,'form': form})
    else:
        try:
            form = PerPodForm(request.POST,instance=pp)
            form.save()
            messages.success(request,"Registro de poder del personaje actualizado con exito")
            return redirect('perpoderes')
        except ValueError:
            return render(request,'act_perpoder.html', {'perpod': pp,'form': form, 'error':"ERROR. No se ha podido actualizar"}) 
        
@login_required
def Permedios(request):
    pm = PersonajeMedio.objects.all()
    return render(request,'permedios.html',{
        'persmed':pm,
    })

@login_required
def elimina_permedio(request,pm_id):
    pm = get_object_or_404(PersonajeMedio,pk=pm_id)
    pm.delete()
    messages.success(request,"Registro del personaje en medio eliminado con exito")
    return redirect('permedios')

@login_required
def new_permedio(request):
    if request.method == 'GET':
        return render(request,'new_permedio.html', {
            'form': PerMedForm,          
        })
    else:
        try:
            form = PerMedForm(request.POST)
            Newpm = form.save(commit=False)
            Newpm.save()
            messages.success(request,"Registro del personaje en medio creado con exito")
            return redirect('permedios')
        except ValueError:
            return render(request,'new_permedio.html', {
                'form': PerMedForm, 
                'error':'Por favor ingrese datos validos'           
            })
        
@login_required
def actualiza_permedio(request,pm_id):
    pm = get_object_or_404(PersonajeMedio,pk=pm_id)
    if request.method == 'GET':
        form = PerMedForm(instance=pm)
        return render(request,'act_permedio.html', {'permed': pm,'form': form})
    else:
        try:
            form = PerMedForm(request.POST,instance=pm)
            form.save()
            messages.success(request,"Registro del personaje en medio actualizado con exito")
            return redirect('permedios')
        except ValueError:
            return render(request,'act_permedio.html', {'permed': pm,'form': form, 'error':"ERROR. No se ha podido actualizar"}) 
        

@login_required
def Perobjetos(request):
    po = PersonajeObjeto.objects.all()
    return render(request,'perobjetos.html',{
        'persobj':po,
    })

@login_required
def elimina_perobjeto(request,po_id):
    po = get_object_or_404(PersonajeObjeto,pk=po_id)
    po.delete()
    messages.success(request,"Registro de objeto del personaje eliminado con exito")
    return redirect('perobjetos')

@login_required
def new_perobjeto(request):
    if request.method == 'GET':
        return render(request,'new_perobjeto.html', {
            'form': PerObjForm,          
        })
    else:
        try:
            form = PerObjForm(request.POST)
            Newpo = form.save(commit=False)
            Newpo.save()
            messages.success(request,"Registro de objeto del personaje creado con exito")
            return redirect('perobjetos')
        except ValueError:
            return render(request,'new_perobjeto.html', {
                'form': PerObjForm, 
                'error':'Por favor ingrese datos validos'           
            })
        
@login_required
def actualiza_perobjeto(request,po_id):
    po = get_object_or_404(PersonajeObjeto,pk=po_id)
    if request.method == 'GET':
        form = PerObjForm(instance=po)
        return render(request,'act_perobjeto.html', {'perpod': po,'form': form})
    else:
        try:
            form = PerObjForm(request.POST,instance=po)
            form.save()
            messages.success(request,"Registro de objeto del personaje actualizado con exito")
            return redirect('perobjetos')
        except ValueError:
            return render(request,'act_perobjeto.html', {'perpod': po,'form': form, 'error':"ERROR. No se ha podido actualizar"}) 

@login_required
def recom_perfavs(request):
    per = get_object_or_404(Perfil,fk_usuario=request.user,esta_activo=True)
    med = Medio.objects.raw("select m.medio_id, medfecestreno, medcomcreacion, medcomproduc, medrating, medsinopsis, medionombre, tipomed from infopersonajes.medio m where m.medio_id in (select pm.fk_med_pers_id from infopersonajes.personaje_medio pm where pm.fk_pers_med_id in ( select pm.fk_pers_med_id from infopersonajes.personaje_medio pm where fk_med_pers_id in ( select fk_med_perf_id from infousuarios.perfil_medio where fk_perf_med_id ="+str(per.per_id)+"))) and m.medio_id not in ( select fk_med_perf_id from infousuarios.perfil_medio where fk_perf_med_id ="+str(per.per_id)+");")
    return render(request,'perfavs.html',{
        'medios':med,
    })

@login_required
def recom_orgfavs(request):
    per = get_object_or_404(Perfil,fk_usuario=request.user,esta_activo=True)
    med = Medio.objects.raw("select m.medio_id, medfecestreno, medcomcreacion, medcomproduc, medrating,  medsinopsis, medionombre, tipomed from infopersonajes.medio m where m.medio_id in (select om.fk_med_org_id from infopersonajes.organizacion_medio om where om.fk_org_med_id in ( select om.fk_org_med_id from infopersonajes.organizacion_medio om where om.fk_med_org_id in ( select fk_med_perf_id from infousuarios.perfil_medio where fk_perf_med_id = "+str(per.per_id)+"))) and  m.medio_id not in ( select fk_med_perf_id from infousuarios.perfil_medio where fk_perf_med_id ="+str(per.per_id)+");")
    return render(request,'orgfavs.html',{
        'medios':med,
    })

@login_required
def Orgmedios(request):
    om = OrganizacionMedio.objects.all()
    return render(request,'orgmedios.html',{
        'orgsmed':om,
    })

@login_required
def elimina_orgmedio(request,om_id):
    om = get_object_or_404(OrganizacionMedio,pk=om_id)
    om.delete()
    messages.success(request,"Registro de la organización en medio eliminado con exito")
    return redirect('orgmedios')

@login_required
def new_orgmedio(request):
    if request.method == 'GET':
        return render(request,'new_orgmedio.html', {
            'form': OrgMedForm,          
        })
    else:
        try:
            form = OrgMedForm(request.POST)
            Newom = form.save(commit=False)
            Newom.save()
            messages.success(request,"Registro de la organización en medio creado con exito")
            return redirect('orgmedios')
        except ValueError:
            return render(request,'new_orgmedio.html', {
                'form': OrgMedForm, 
                'error':'Por favor ingrese datos validos'           
            })
        
@login_required
def actualiza_orgmedio(request,om_id):
    om = get_object_or_404(OrganizacionMedio,pk=om_id)
    if request.method == 'GET':
        form = OrgMedForm(instance=om)
        return render(request,'act_orgmedio.html', {'orgmed': om,'form': form})
    else:
        try:
            form = OrgMedForm(request.POST,instance=om)
            form.save()
            messages.success(request,"Registro de la organización en medio actualizado con exito")
            return redirect('orgmedios')
        except ValueError:
            return render(request,'act_orgmedio.html', {'orgmed': om,'form': form, 'error':"ERROR. No se ha podido actualizar"}) 
        
@login_required
def Nacionalidades(request):
    nac = Nacionalidad.objects.all()
    return render(request,'nacionalidades.html',{
        'naciones':nac,
    })

@login_required
def elimina_nacionalidad(request,nac_id):
    nac = get_object_or_404(Nacionalidad,pk=nac_id)
    nac.delete()
    messages.success(request,"Nacionalidad eliminada con exito")
    return redirect('nacionalidades')

@login_required
def new_nacionalidad(request):
    if request.method == 'GET':
        return render(request,'new_nacionalidad.html', {
            'form': NacForm,          
        })
    else:
        try:
            form = NacForm(request.POST)
            NewNac = form.save(commit=False)
            NewNac.save()
            messages.success(request,"Nacionalidad creada con exito")
            return redirect('nacionalidades')
        except ValueError:
            return render(request,'new_nacionalidad.html', {
                'form': NacForm, 
                'error':'Por favor ingrese datos validos'           
            })
        
@login_required
def actualiza_nacionalidad(request,nac_id):
    nac = get_object_or_404(Nacionalidad,pk=nac_id)
    if request.method == 'GET':
        form = NacForm(instance=nac)
        return render(request,'act_nacionalidad.html', {'nacion': nac,'form': form})
    else:
        try:
            form = NacForm(request.POST,instance=nac)
            form.save()
            messages.success(request,"Nacionalidad actualizada con exito")
            return redirect('nacionalidades')
        except ValueError:
            return render(request,'act_nacionalidad.html', {'nacion': nac,'form': form, 'error':"ERROR. No se ha podido actualizar"}) 

@login_required
def Ocupaciones(request):
    ocu = Ocupacion.objects.all()
    return render(request,'ocupaciones.html',{
        'ocupas':ocu,
    })

@login_required
def elimina_ocupacion(request,ocu_id):
    ocu = get_object_or_404(Ocupacion,pk=ocu_id)
    ocu.delete()
    messages.success(request,"Ocupación eliminada con exito")
    return redirect('ocupaciones')

@login_required
def new_ocupacion(request):
    if request.method == 'GET':
        return render(request,'new_ocupacion.html', {
            'form': OcuForm,          
        })
    else:
        try:
            form = OcuForm(request.POST)
            NewOcu = form.save(commit=False)
            NewOcu.save()
            messages.success(request,"Ocupación creada con exito")
            return redirect('ocupaciones')
        except ValueError:
            return render(request,'new_ocupacion.html', {
                'form': OcuForm, 
                'error':'Por favor ingrese datos validos'           
            })
        
@login_required
def actualiza_ocupacion(request,ocu_id):
    ocu = get_object_or_404(Ocupacion,pk=ocu_id)
    if request.method == 'GET':
        form = OcuForm(instance=ocu)
        return render(request,'act_ocupacion.html', {'ocupa': ocu,'form': form})
    else:
        try:
            form = OcuForm(request.POST,instance=ocu)
            form.save()
            messages.success(request,"Ocupación actualizada con exito")
            return redirect('ocupaciones')
        except ValueError:
            return render(request,'act_ocupacion.html', {'ocupa': ocu,'form': form, 'error':"ERROR. No se ha podido actualizar"}) 

@login_required
def Creadores(request):
    cre = Creador.objects.all()
    return render(request,'creadores.html',{
        'cread':cre,
    })

@login_required
def elimina_creador(request,cre_id):
    cre = get_object_or_404(Creador,pk=cre_id)
    cre.delete()
    messages.success(request,"Creador eliminado con exito")
    return redirect('creadores')

@login_required
def new_creador(request):
    if request.method == 'GET':
        return render(request,'new_creador.html', {
            'form': CreForm,          
        })
    else:
        try:
            form = CreForm(request.POST)
            NewCre = form.save(commit=False)
            NewCre.save()
            messages.success(request,"Creador registrado con exito")
            return redirect('creadores')
        except ValueError:
            return render(request,'new_creador.html', {
                'form': CreForm, 
                'error':'Por favor ingrese datos validos'           
            })
        
@login_required
def actualiza_creador(request,cre_id):
    cre = get_object_or_404(Creador,pk=cre_id)
    if request.method == 'GET':
        form = CreForm(instance=cre)
        return render(request,'act_creador.html', {'crea': cre,'form': form})
    else:
        try:
            form = CreForm(request.POST,instance=cre)
            form.save()
            messages.success(request,"Creador actualizado con exito")
            return redirect('creadores')
        except ValueError:
            return render(request,'act_creador.html', {'crea': cre,'form': form, 'error':"ERROR. No se ha podido actualizar"}) 