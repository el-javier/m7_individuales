from django.contrib import admin
from .models import Etiqueta

# Register your models here.

class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

admin.site.register(Etiqueta)