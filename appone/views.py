from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import login,logout, authenticate
from django.db import IntegrityError
from .forms import *
from .models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
# Create your views here.

class Index(TemplateView):
            template_name = "index.html"

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
            if user.sub_fk:
                return redirect('home')
            else:
                return redirect('sub')

@login_required
def singout(request):
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
        comtdc = Tarjetacredito.objects.filter(fk_usuario=request.user)
        if comtdc:
            return redirect('home')
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
            return redirect('home')
        except ValueError:
            return render(request,'registrar_tarjeta.html', {
                'form': TDCForm,
                'error':'Por favor ingrese datos validos'           
            })
        
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