from django.shortcuts import render
from futbol.models import *

def classificacio(request):
    lliga = Lliga.objects.all()[1]
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
