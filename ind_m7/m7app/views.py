from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Tarea
from .forms import TareaForm
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

# definir vista de tareas pendientes
@login_required
def listar_tareas(request):
    tareas_pendientes = Tarea.objects.filter(usuario=request.user, estado='pendiente').order_by('fecha_vencimiento')
    tareas_completadas = Tarea.objects.filter(estado='completada').order_by('-fecha_vencimiento')


    return render(request, 'lista_tareas.html', {'tareas_pendientes': tareas_pendientes, 'tareas_completadas': tareas_completadas})

def crear_tarea(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.usuario = request.user  # Asigna el usuario actual a la tarea
            tarea.save()
            return redirect('listar_tareas')
    else:
        form = TareaForm()
    return render(request, 'crear_tarea.html', {'form': form})

# def ver_tarea(request, tarea_id):
#     tarea = Tarea.objects.get(id=tarea_id)
#     return render(request, 'ver_tarea.html', {'tarea': tarea})


def ver_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    return render(request, 'ver_tarea.html', {'tarea': tarea})

def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('ver_tarea', tarea_id=tarea.id)
    else:
        form = TareaForm(instance=tarea)

    return render(request, 'editar_tarea.html', {'form': form, 'tarea': tarea})

def confirmar_eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    if request.method == 'POST':
        tarea.delete()
        return redirect('listar_tareas')

    return render(request, 'confirmar_eliminar_tarea.html', {'tarea': tarea})

def completar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    if tarea.estado != 'completada':
        tarea.estado = 'completada'
        tarea.save()

    return redirect('ver_tarea', tarea_id=tarea.id)

