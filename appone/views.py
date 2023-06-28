from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import login,logout, authenticate
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
    act = Actividad.objects.create(act_ingreso=timezone.now(),fk_perfil=perf)
    act.save()
    return redirect('home')

@login_required
def Civiles(request):
    civiles = Personaje.objects.raw(
        "select p.personaje_id, genc, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, color_pelo,color_ojos, frase_celebre, comic_primer_vez, estadomarital from infopersonajes.personaje p inner join infopersonajes.civil c on p.personaje_id = c.personaje_id")
    return render(request,'civiles.html',{
        'civiles':civiles
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
            return redirect('civiles')
        except ValueError:
            return render(request,'new_civil.html', {
                'form': PersonajeForm,
                'error':'Por favor ingrese datos validos'           
            })
        

@login_required
def elimina_civil(request,civil_id):
    civ = Civil.objects.filter(personaje=civil_id)
    pers = Personaje.objects.filter(personaje_id=civil_id)
    civ.delete()
    pers.delete()
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
    hero = get_object_or_404(Heroe,pk=heroe_id)
    pers = get_object_or_404(Personaje,pk=heroe_id)
    hero.delete()
    pers.delete()
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
    vil.delete()
    pers.delete()
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
    pel.delete()
    med.delete()
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
            NewPel.save()
            peli.medio = NewPel
            peli.save()
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
    ser.delete()
    med.delete()
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
            NewSer.save()
            ser.medio = NewSer
            ser.save()
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
    jue.delete()
    med.delete()
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
            NewJue.save()
            jue.medio = NewJue
            jue.save()
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
    org = get_object_or_404(Organizacion,pk=org_id)
    org.delete()
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
    sed = get_object_or_404(Sede,pk=sed_id)
    sed.delete()
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
    pod = get_object_or_404(Poder,pk=pod_id)
    pod.delete()
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
    obj = get_object_or_404(Objeto,pk=obj_id)
    obj.delete()
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
    return redirect('listguardados')

@login_required
def lg_guardar(request,med_id):
    per = get_object_or_404(Perfil,fk_usuario=request.user,esta_activo=True)
    med = get_object_or_404(Medio,pk=med_id)
    Permed = PerfilMedio.objects.create(fk_perf_med=per,fk_med_perf=med,fecha_vista=timezone.now())
    Permed.save()
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
