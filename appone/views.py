from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm,UsuarioForm,LoginForm,TDCForm
from .models import Task,Usuario
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
                return redirect('home')
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
            return redirect('home')
        
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