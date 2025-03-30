from django.contrib import admin
from .models import CustomUser,Contrato,Proyecto,SeguimientoTiempo,Tarea
# Register your models here.

@admin.register(CustomUser)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'fecha_creacion') 
    search_fields = ('nombre', 'correo')
#admin.site.register(Usuario, UsuarioAdmin)

@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('nombre_cliente', 'fecha_inicio', 'fecha_fin', 'fecha_creacion')
#admin.site.register(Contrato, ContratoAdmin)

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display=('nombre', 'descripcion','fecha_inicio', 'fecha_fin', 'fecha_creacion')
#admin.site.register(Proyecto, ProyectoAdmin)

@admin.register(SeguimientoTiempo)
class SeguimientoTiempoAdmin(admin.ModelAdmin):
    list_display=('id_tarea', 'inicio', 'fin', 'duracion', 'fecha_creacion')
#admin.site.register(SeguimientoTiempo, SeguimientoTiempoAdmin)

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display=('id_proyecto', 'nombre','descripcion','estado','fecha_creacion')
#admin.site.register(Tarea, TareaAdmin)