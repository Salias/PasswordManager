# -*- coding: utf-8 -*-

def desactivar_usuario(modeladmin, request, queryset):
    for obj in queryset:
        obj.is_active = False   
        #Guardamos en la BBDD
        obj.save()
desactivar_usuario.short_description = "Desactivar Usuario"

def activar_usuario(modeladmin, request, queryset):
    for obj in queryset:
        obj.is_active = True
        #Guardamos en la BBDD
        obj.save()
activar_usuario.short_description = "Activar usuario"
