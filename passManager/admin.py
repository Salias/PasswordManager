# -*- coding: utf-8 -*-
from django.contrib import admin
from passManager.models import passDb, passEncr
from django.contrib.admin import SimpleListFilter


class loginsFilter(SimpleListFilter):
    ''' Filtro para el admin basado en los
    logins. Se hace facetado de los resultados
    y solo muestra aquellos logins que tienen
    mas de 1 aparicion'''
    title = "TOP Logins"
    parameter_name = "logins"
    # Get all objects
    rows = passDb.objects.all()                                                                                                                                                      
    # Logins list                                                                                                                                                     
    logins = []                                                                                                                                                                      
    for row in rows:
        logins.append(row.login)                                                                                                                                                     
    # Duplicate clean
    logins = set(logins)                                                                                                                                                             
    
    # Get tuple with login and ocurences
    lista = {}
    for l in set(logins):
        numrows = passDb.objects.filter(login=l).count()                                                                                                                                      
        if numrows > 2:
            lista[str(l)] = numrows                                                                                                                                                  
                                                                                                                                                                                 
    # Import module for order dictionary                                                                                                                                                
    from operator import itemgetter                                                                                                                                                  
    slist = sorted(lista.items(), key=itemgetter(1), reverse=True)                                                                                                                   
    
    # Generate facetes
    facet = []                                                                                                                                                                       
    for n in range(0 ,(len(slist))):
        facet.append(((slist[n][0]),(slist[n][0]+' ('+str(slist[n][1]))+')'))
    
    def lookups(self, request, model_admin):
        return (
                self.facet
#                ('roots', u"roots"),
#                ('admins', u"admins"),
                )
        
    def queryset(self, request, queryset):
        for n in range(0 ,(len(self.slist))):
            val = self.slist[n][0]
            if self.value() == val:
                return queryset.filter(login=val)


class passManagerAdmin(admin.ModelAdmin):
    class Media:
        js = ("js/jquery-1.7.1.min.js", "js/jquery-ui-1.8.18.custom.min.js", "js/functions.js",)
        css = {
            "all": ("css/jquery-ui-1.8.18.custom.css",)
        }
        
    list_per_page = 20
    actions = ['export_as_json']    
    actions_on_bottom = True
    actions_on_top = False
    list_display = ('name','login','getClickMe','server','uploader','date','notes','send_email_html')
    fieldsets = [
                 (None,         {'fields': ['name',('login','password'),'server','notes']}),
                 ]
    search_fields = ['name','login','server','notes']
        
    def save_model(self, request, obj, form, change):
        obj.password = passEncr('encrypt', obj.password)
        obj.uploader = request.user
        obj.nivel = 1
        obj.save()
    
    def get_list_filter(self, request):
        if request.user.is_superuser or request.user.groups.filter(name='GrupoAdministrador').exists():
            return (loginsFilter,'uploader','date')
        return ('date',)
    
    def queryset(self, request):
        """Función que listará todas las contraseñas de todos los usuarios activos 
        en el caso de que el usuario tengo el rol de Administrador y sólo las suyas en caso de que sea un usuario.
        """
        qset = passDb.objects.none()
        qs = super(passManagerAdmin, self).queryset(request)
        if  request.user.is_superuser or request.user.groups.filter(name='GrupoAdministrador').exists():
            qset = qs
        else:
            qset = qs.filter(uploader=request.user)
    
        excludes = []
        for q in qset:
            if not q.uploader.is_active: 
                excludes.append(q.id)
        print excludes
        return qset.exclude(id__in=excludes)
    
    def send_email_html(self, queryset):
        buttons = """                                                                                                                                                            
            <div style="width:20px">                                                                                                                                             
            <a href="/send_pass/%s" title="Enviar por Email" name="Envio de Correo" class="mailwindow"><img src="/static/images/mail-message-new.png"></img></a>                       
            </div>
        """ % (queryset.id)
        return buttons
    send_email_html.short_description = ''
    send_email_html.allow_tags = True
    
    def export_as_json(self, request, queryset):
        from django.http import HttpResponse
        from django.core import serializers
        response = HttpResponse(mimetype="text/javascript")
        serializers.serialize("json", queryset, stream=response)
        return response

        
admin.site.register(passDb, passManagerAdmin)
