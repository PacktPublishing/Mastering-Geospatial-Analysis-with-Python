from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from .models import US_States, Counties, Districts, Arenas
from .forms import ArenaForm

from django.views.decorators.http import require_http_methods
import random

@require_http_methods(["GET", "POST"])
def index(request):
	return redirect(arena)


def queryarena(name):
        arena = Arenas.objects.filter(name1=name)[0]
        state = US_States.objects.filter(geom__intersects=arena.geom)
        if state:
                state = state[0]
                county = Counties.objects.filter(geom__contains=arena.geom)[0]
                district = Districts.objects.filter(geom__contains=arena.geom)[0]
                popup = "This arena is called " + arena.name1 + " and it's located at " 
                popup += str(round(arena.geom.x,5))+ "," + str(round(arena.geom.y,5) ) 
                popup += ". It is located in " +state.state + " and in the county of " + county.county
                popup += " and in Congressional District " + district.district
                return arena.name1, arena.geom.y, arena.geom.x, popup
        else:
                return arena.name1, arena.geom.y, arena.geom.x, "This is located outside of the United States"
        

@require_http_methods(["GET", "POST"])
def arena(request):
        values = Arenas.objects.values_list('id','name1')
        if request.method=="GET":
                form = ArenaForm(request.GET)
                names = [name for ids, name in values]
                length = len(names)
                selectname = names[random.randint(0, length-1)]
                form.name, form.latitude, form.longitude, form.popup = queryarena(selectname)
                return render(request, "arena/index.html", {"form":form})
        else:
                form= ArenaForm(request.POST)
                if form.is_valid():
                        selectid = int(request.POST['selections'])
                        selectname = [name for ids, name in values if ids == selectid][0]
                        form.name, form.latitude, form.longitude, form.popup = queryarena(selectname)
                        return render(request, "arena/index.html", {"form":form})

