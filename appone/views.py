from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,logout, authenticate
from django.db import IntegrityError
from .forms import *
from .models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


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
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request,'Tasks.html',{
        'tasks':tasks
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False)
    return render(request,'Tasks.html',{
        'tasks':tasks
    })

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request,'create_task.html', {
            'form': TaskForm,           
        })
    else:
        try:
            form = TaskForm(request.POST)
            Newtask = form.save(commit=False)
            Newtask.user = request.user
            Newtask.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'create_task.html', {
                'form': TaskForm,
                'error':'Por favor ingrese datos validos'           
            })
        
@login_required
def task_detail(request,task_id):
    task = get_object_or_404(Task,pk=task_id, user=request.user)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request,'task_detail.html', {'task': task,'form': form })
    else:
        try:
            form = TaskForm(request.POST,instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'task_detail.html', {'task': task,'form': form,
                'error':"ERROR. No se ha podido actualizar la tarea"
            })
        
@login_required
def complete_task(request,task_id):
    task = get_object_or_404(Task,pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
    
@login_required
def delete_task(request,task_id):
    task = get_object_or_404(Task,pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def singout(request):
    logout(request)
    return redirect('home')

@login_required
def seleccionar_subscripcion(request):
    if request.method == 'GET':
        return render(request,'select_sub.html')

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
        "select p.id_personaje, genc, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, color_pelo,color_ojos, frase_celebre, comic_primer_vez, estadomarital from infopersonajes.personaje p inner join infopersonajes.civil c on p.id_personaje = c.id_personaje")
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
            NewCiv.id_personaje = NewCiv.id_personaje
            civil = Civil(id_personaje = NewCiv.id_personaje)
            NewCiv.save()
            civil.save()
            return redirect('civiles')
        except ValueError:
            return render(request,'new_civil.html', {
                'form': TaskForm,
                'error':'Por favor ingrese datos validos'           
            })
        

@login_required
def elimina_civil(request,civil_id):
    civ = get_object_or_404(Civil,pk=civil_id)
    pers = get_object_or_404(Personaje,pk=civil_id)
    if request.method == 'POST':
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