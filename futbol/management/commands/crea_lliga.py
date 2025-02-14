from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from datetime import timedelta
from random import randint, choice
 
from futbol.models import *
 
faker = Faker(["es_CA", "es_ES"])
 
class Command(BaseCommand):
    help = 'Crea una lliga amb equips i jugadors'
 
    def add_arguments(self, parser):
        parser.add_argument('titol_lliga', nargs=1, type=str)
 
    def handle(self, *args, **options):
        titol_lliga = options['titol_lliga'][0]
        lliga = Lliga.objects.filter(nom=titol_lliga)
        if lliga.exists():
            print("Aquesta lliga ja està creada. Posa un altre nom.")
            return
 
        print(f"Creem la nova lliga: {titol_lliga}")
        lliga = Lliga(nom=titol_lliga)
        lliga.save()
 
        print("Creem equips")
        prefixos = ["RCD", "Athletic", "", "Deportivo", "Unión Deportiva"]
        for _ in range(20):
            ciutat = faker.city()
            prefix = choice(prefixos)
            nom = f"{prefix} {ciutat}".strip()
            any_fundacio = randint(1900, 2020)
            equip = Equip(ciutat=ciutat, nom=nom, lliga=lliga, any_fundacio=any_fundacio)
            equip.save()
 
            print(f"Creem jugadors de l'equip {nom}")
            posicions = ['PT', 'DF', 'MC', 'DL']
            for _ in range(25):
                nom = faker.name()
                posicio = choice(posicions)
                dorsal = randint(1, 99)
                nacionalitat = faker.country()
                jugador = Jugador(nom=nom, posicio=posicio, equip=equip, dorsal=dorsal, nacionalitat=nacionalitat)
                jugador.save()
 
        print("Creem partits de la lliga")
        for local in lliga.equips.all():
            for visitant in lliga.equips.all():
                if local != visitant:
                    data_partit = timezone.now() - timedelta(days=randint(0, 365))
                    partit = Partit(equip_local=local, equip_visitant=visitant, lliga=lliga, data=data_partit)
                    partit.save()

                    print(f"Generant esdeveniments per al partit {local.nom} vs {visitant.nom}")
                    
                    # Crear de 0 a 5 gols per partit
                    for _ in range(randint(0, 10)):

                        # elegir el equipo que marca el gol
                        equip_golejador = choice([local, visitant])

                        # elegir el jugador que mete el gol
                        jugador = choice(equip_golejador.jugadors.all())

                        # crear un minuto
                        minut = randint(1, 90)

                        # crear un Evento (bd)
                        event = Event(partit=partit, jugador=jugador, tipus_esdeveniment='gol', minut=minut)

                        # guardar el evento
                        event.save()

                        #imprimir por consola el gol
                        print(f"Gol de {jugador.nom} al minut {minut} per {equip_golejador.nom}")

        print("S'ha completat la creació de la lliga amb equips, jugadors i partits.")
