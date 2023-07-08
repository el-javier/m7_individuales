"""
URL configuration for primer_proyecto project.

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
from django.contrib.auth import views as auth_views
from django.urls import path
from m7app.views import login_view, logout_view, home, listar_tareas, crear_tarea, ver_tarea, editar_tarea, confirmar_eliminar_tarea, completar_tarea, editar_prioridad

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', login_view, name='login'),
    path('tareas/', listar_tareas, name='listar_tareas'),
    path('tareas/crear/', crear_tarea, name='crear_tarea'),
    path('tareas/ver/<int:tarea_id>/', ver_tarea, name='ver_tarea'),
    path('tareas/editar/<int:tarea_id>/', editar_tarea, name='editar_tarea'),
    path('tareas/eliminar/<int:tarea_id>/', confirmar_eliminar_tarea, name='confirmar_eliminar_tarea'),
    path('tareas/completar/<int:tarea_id>/', completar_tarea, name='completar_tarea'),
    path('tareas/editar_prioridad/<int:tarea_id>/', editar_prioridad, name='editar_prioridad'),

]