"""
URL configuration for lligaFutbol project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from futbol import views

urlpatterns = [
    # path('classificacio/',views.classificacio ),
    path('admin/', admin.site.urls),
    path("", views.menu, name="menu"), #en la raíz te lleva al menú
    path("nou_jugador",views.nou_jugador, name="nou_jugador"),
    path("classificacio/<int:lliga_id>", views.classificacio, name="classificacio"), #obligar a pasarle un número (int)
    path("jugadors", views.jugadors, name="jugadors"),
    path("matriu_gols/<int:lliga_id>/", views.matriu_gols, name="matriu_gols"),
]
