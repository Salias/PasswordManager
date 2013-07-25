# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class Usuario (User):
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'usuarios' 
        
    def __unicode__(self):
        return unicode(self.username)

class Administrador (models.Model):
    class Meta:
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores' 
            
    user = ForeignKey(Usuario, unique=True)
    
    def save(self, force_insert=False, force_update=False, using=None):
        models.Model.save(self, force_insert=force_insert, force_update=force_update, using=using)
        self.user.groups.add(Group.objects.select_related().get(name='GrupoAdministrador'))
        self.user.is_staff = True
        self.user.save()
                   
    def eliminar(self):                          
        self.user.groups.remove(Group.objects.select_related().get(name='GrupoAdministrador'))
        self.user.save()
        
    def __unicode__(self):
        return unicode(self.user)
          
        
@receiver(pre_delete, sender=Usuario)
def delete_usuario(sender, instance, **kwargs):
    instance.eliminar()
    
@receiver(pre_delete, sender=Administrador)
def delete_administrador(sender, instance, **kwargs):
    instance.eliminar()      


# Clase obligatoria para la interfaz de administración
class Admin:
    pass
