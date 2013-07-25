# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import Group
from users.models import Usuario, Administrador
from django.contrib.auth.admin import UserAdmin
from users.actions import desactivar_usuario, activar_usuario
    

class UsuarioAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ( ('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        ( ('Permissions'), {'fields': ('is_active', 'is_staff')}),        
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')}
        ),
    )         
    actions = [desactivar_usuario, activar_usuario]
     
    def save_model(self, request, obj, form, change): 
        obj.save() 
        obj.groups.add(Group.objects.get(name='GrupoUsuario'))
        obj.is_staff = True                  
        obj.save()
     
    def get_list_display(self, request):
        return ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
        
    def get_actions(self, request):
        actions = super(UsuarioAdmin, self).get_actions(request)
        if request.user.groups.filter(name="GrupoAdministradorusuarios").exists():
            del actions['delete_selected']
        return actions     
         

admin.site.register(Administrador)
admin.site.register(Usuario, UsuarioAdmin)