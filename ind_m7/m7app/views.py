from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Tarea, Etiqueta
from .forms import TareaForm, ObservacionForm, PrioridadForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

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

# def listar_tareas(request):
#     tareas_pendientes = Tarea.objects.filter(usuario=request.user, estado='pendiente').order_by('fecha_vencimiento')
#     tareas_completadas = Tarea.objects.filter(estado='completada').order_by('-fecha_vencimiento')


#     return render(request, 'lista_tareas.html', {'tareas_pendientes': tareas_pendientes, 'tareas_completadas': tareas_completadas})

# def listar_tareas(request):
#     tareas_pendientes = Tarea.objects.filter(estado='pendiente').order_by('fecha_vencimiento')
#     tareas_completadas = Tarea.objects.filter(estado='completada').order_by('-fecha_vencimiento')
#     etiquetas = Etiqueta.objects.all()

#     return render(request, 'lista_tareas.html', {'tareas_pendientes': tareas_pendientes, 'tareas_completadas': tareas_completadas})
@login_required
def listar_tareas(request):
    etiqueta_id = request.GET.get('etiqueta')  # Obtener el valor del filtro de etiqueta

    # Filtrar las tareas pendientes según la etiqueta seleccionada (si existe)
    usuario_actual = request.user
    tareas_pendientes = Tarea.objects.filter(estado='pendiente', asignado_a=usuario_actual)
    tareas_completadas = Tarea.objects.filter(estado='completada', asignado_a=usuario_actual).order_by('-fecha_vencimiento')
    if etiqueta_id:
        tareas_pendientes = tareas_pendientes.filter(etiqueta_id=etiqueta_id)

    # Ordenar las tareas pendientes por prioridad y luego por fecha de vencimiento
    tareas_pendientes = tareas_pendientes.order_by('fecha_vencimiento')

    etiquetas = Etiqueta.objects.all()
    prioridades = ['alta', 'media', 'baja']  # Agrega las opciones de prioridad aquí

    return render(request, 'lista_tareas.html', {'tareas_pendientes': tareas_pendientes, 'etiquetas': etiquetas, 'tareas_completadas': tareas_completadas, 'prioridades': prioridades,})


def crear_tarea(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.usuario = form.cleaned_data['asignado_a']
            tarea.save()
            return redirect('listar_tareas')
    else:
        form = TareaForm()
    return render(request, 'crear_tarea.html', {'form': form})

# def ver_tarea(request, tarea_id):
#     tarea = Tarea.objects.get(id=tarea_id)
#     return render(request, 'ver_tarea.html', {'tarea': tarea})


# def ver_tarea(request, tarea_id):
#     tarea = get_object_or_404(Tarea, id=tarea_id)

#     return render(request, 'ver_tarea.html', {'tarea': tarea})


def ver_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    usuario_asignado = tarea.asignado_a  # Obtén el usuario asignado a la tarea

    # Verificar si la tarea pertenece al usuario actual
    if tarea.asignado_a != request.user:
        return HttpResponseForbidden()  # Devolver un error de acceso prohibido

    if request.method == 'POST':
        form = ObservacionForm(request.POST)
        if form.is_valid():
            observacion = form.cleaned_data['observacion']
            tarea.observaciones = observacion
            tarea.save()
            return redirect('ver_tarea', tarea_id=tarea.id)
    else:
        form = ObservacionForm(initial={'observacion': tarea.observaciones})  # Agregar observación guardada al formulario

    return render(request, 'ver_tarea.html', {'tarea': tarea, 'usuario_asignado': usuario_asignado, 'form': form})



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

# def completar_tarea(request, tarea_id):
#     tarea = get_object_or_404(Tarea, id=tarea_id)

#     if tarea.estado != 'completada':
#         tarea.estado = 'completada'
#         tarea.save()

#     return redirect('ver_tarea', tarea_id=tarea.id)

def completar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    if tarea.estado != 'completada':
        tarea.estado = 'completada'
        tarea.save()

    return redirect('listar_tareas')

from django.http import JsonResponse

# def actualizar_prioridad_tarea(request, tarea_id):
#     tarea = get_object_or_404(Tarea, id=tarea_id)

#     if request.method == 'POST':
#         prioridad = request.POST.get('prioridad')
#         tarea.prioridad = prioridad
#         tarea.save()
#         return JsonResponse({'success': True})

#     return JsonResponse({'success': False})

def editar_prioridad(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    if request.method == 'POST':
        form = PrioridadForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('listar_tareas')  # Redirecciona nuevamente a la página de listar tareas
    else:
        form = PrioridadForm(instance=tarea)

    return render(request, 'editar_prioridad.html', {'form': form, 'tarea': tarea})
