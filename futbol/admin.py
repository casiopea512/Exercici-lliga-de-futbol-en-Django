from django.contrib import admin

# Register your models here.
from futbol.models import *

admin.site.register(Lliga)
admin.site.register(Equip)
admin.site.register(Jugador)

class EventInLine(admin.TabularInline): # es lo que vas a añadir dentro de la vista editar
    model = Event
    Extra = 2

class PartitAdmin(admin.ModelAdmin): # modificar cómo vemos Partit
    list_display = ('equip_local','equip_visitant','data', 'gols_locals', 'gols_visitants') # esto modifica cómo se ven las tablas fuera
    fields = ("lliga","equip_local",'equip_visitant','data','gols_locals','gols_visitants')
    readonly_fields = ('gols_locals','gols_visitants') # mostra però no deixa modificar

    search_fields = ('equip_local__nom','equip_visitant__nom')

    # aunque parezca que solo llama a clases, también a funciones como mostrar los goles
    inlines = [EventInLine,] # esto modifica cómo se ve al editar o crear un partido

admin.site.register(Partit, PartitAdmin)