from django.shortcuts import render
from django.shortcuts import redirect
from futbol.models import *
from django import forms

def classificacio(request,lliga_id): # a la view de classificació le llega el request y la lliga_id desde la view de 'menú' 
    lliga = Lliga.objects.get(id=lliga_id)
    equips = lliga.equips.all()
    classi = []

    for equip in equips:
        punts = 0
        victories = 0
        derrotes = 0
        empats = 0
        gols_favor = 0
        gols_contra = 0

        # Partits com a equip local
        for partit in lliga.partits.filter(equip_local=equip):
            gols_locals = partit.gols_locals()
            gols_visitants = partit.gols_visitants()

            gols_favor += gols_locals
            gols_contra += gols_visitants

            if gols_locals > gols_visitants:
                punts += 3
                victories += 1
            elif gols_locals == gols_visitants:
                empats += 1
                punts += 1
            else:
                derrotes += 1

        # Partits com a equip visitant
        for partit in lliga.partits.filter(equip_visitant=equip):
            gols_locals = partit.gols_locals()
            gols_visitants = partit.gols_visitants()

            gols_favor += gols_visitants
            gols_contra += gols_locals

            if gols_locals < gols_visitants:
                victories += 1
                punts += 3
            elif gols_locals == gols_visitants:
                empats += 1
                punts += 1
            else:
                derrotes += 1

        # Cálculo de la mitjana de gols per partit
        total_partits = victories + derrotes + empats
        if total_partits > 0:
            mitjana_gols = round(gols_favor / total_partits, 2)
        else:
            mitjana_gols = 0

        classi.append({
            'punts': punts,
            'equip': equip.nom,
            'victories': victories,
            'derrotes': derrotes,
            'empats': empats,
            'gols_favor': gols_favor,
            'gols_contra': gols_contra,
            'mitjana_gols': mitjana_gols
        })

    classi.sort(reverse=True, key=lambda x: x['punts'])

    return render(request, "classificacio.html", {
        'lliga': lliga,
        "classificacio": classi,
    })

class MenuForm(forms.Form):
    #query que creas con el nombre lligueta
    lligueta = forms.ModelChoiceField(queryset=Lliga.objects.all())
    dades = forms.CharField(required=False) # añades en el form más campos, como por ejemplo un campo

class JugadorForm(forms.ModelForm):
    class Meta: # son modificaciones de la clase que no se verán en el formulario
        model = Jugador
        fields = "__all__"

def nou_jugador(request):
    

    if request.method == "POST":
        form = JugadorForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('nou_jugador')
    else:
        form = JugadorForm()
    return render(request, "menu.html", {"form":form})

def menu(request):
    #instanciamos el objeto MenuForm que hemos hecho antes
    form = MenuForm()

    #si se llama a esta view desde post significa que han hecho submit en el form
    if request.method == "POST":
        form = MenuForm(request.POST)

        #comprueba que sea correcto
        if form.is_valid():

            # para acceder a los datos una vez que las ha validado.
            lliga = form.cleaned_data.get("lligueta")
            # cridem a /classificacio/<lliga_id>
            return redirect('classificacio',lliga.id)
        
    return render(request, "menu.html",{
                    "form": form,
            })

def jugadors(request):
    jugadors = Jugador.objects.all()  # Obtener todos los jugadores
    classificacio_gols = []

    for jugador in jugadors:
        gols = jugador.event_set.filter(tipus_esdeveniment="gol").count()
        classificacio_gols.append({
            "nom": jugador.nom,
            "equip": jugador.equip.nom,
            "gols": gols
        })

    # Ordenar por número de goles en orden descendente
    classificacio_gols.sort(key=lambda x: x["gols"], reverse=True)

    return render(request, "jugadors.html", {
        "classificacio_gols": classificacio_gols
    })

def matriu_gols(request, lliga_id):
    lliga = Lliga.objects.get(id=lliga_id)
    equips = list(lliga.equips.all())  # Convertimos el QuerySet en una lista
    partits = lliga.partits.all()

    # Crear un diccionario para almacenar los goles
    resultats = {equip.id: 9{e.id: "" for e in equips} for equip in equips}

    for partit in partits:
        resultats[partit.equip_local.id][partit.equip_visitant.id] = f"{partit.gols_locals()} - {partit.gols_visitants()}"

    # Construir una matriz lista para la tabla
    matriu = []
    for equip_fila in equips:
        fila = [equip_fila.nom]  # Primera celda con el nombre del equipo
        for equip_columna in equips:
            if equip_fila.id == equip_columna.id:
                fila.append("X") # celda en la que coincide el equipo con sí mismo
            else:
                fila.append(resultats[equip_fila.id][equip_columna.id])
        matriu.append(fila)

    return render(request, "matriu_gols.html", {
        "lliga": lliga,
        "equips": equips,
        "matriu": matriu,  # Pasamos la tabla ya lista
    })
