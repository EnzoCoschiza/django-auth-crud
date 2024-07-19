from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
from .forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form' : UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user= User.objects.create_user(username= request.POST['username'], password= request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form' : UserCreationForm,
                    'error' : 'User already exists'
                })
        else:
            return render(request, 'signup.html', {
                    'form' : UserCreationForm,
                    'error' : 'Passwords do not match'
                })

@login_required      
def tasks(request):
    tasksUndone= Task.objects.filter(user= request.user, dateCompleted__isnull=True)
    tasksDone= Task.objects.filter(user= request.user, dateCompleted__isnull=False).order_by('-dateCompleted')
    print(tasksDone)
    return render(request,'tasks.html',{
        'tasksUndone': tasksUndone,
        'tasksDone': tasksDone
    })

@login_required 
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html',{
            'form': TaskForm
        })
    else:
        try:
            #print(request.POST)
            form= TaskForm(request.POST) #Acá pasamos lo que recibimos del post al modelo TaskForm
            new_task= form.save(commit=False) #Aca formamos la nueva tarea en new task con todos sus atributos
            new_task.user= request.user # Aca le añadimos el usuario que por defecto no lo trae el formulario pero si nuestra request
            new_task.save() #Y aca lo subimos a nuestra base de datos como la clase Task
        
            return redirect ('tasks')
        
        except ValueError: 
            #Por si el formulario fue modificado debemos chequearlo
            return render(request, 'create_task.html',{
                'form': TaskForm,
                'error' : 'Please fill the gaps with validate data...'
            })

@login_required 
def task_detail(request,task_id):
    if request.method == 'GET':
        task= get_object_or_404(Task, pk=task_id, user= request.user)
        form = TaskForm(instance= task)
        return render(request, 'task_detail.html',{
            'task' : task,
            'form' : form,
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form= TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html',{
                'task': task,
                'form': form,
                'error': 'Updating error...'
            })

@login_required 
def delete_task(request, task_id):
    task= get_object_or_404(Task, pk= task_id, user= request.user)
    task.delete()
    return redirect('tasks')

@login_required 
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user= request.user)
    task.dateCompleted = timezone.now()
    task.save()
    return redirect('tasks')

@login_required 
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form':AuthenticationForm,
        })
    else: 
        user= authenticate(request, username= request.POST['username'], password= request.POST['password'])
        
        if user is not None:
            login(request,user)
            return redirect("tasks")
        else:
            return render(request, 'signin.html',{
                'form':AuthenticationForm,
                'error': 'User or password is incorrect'
            })
        